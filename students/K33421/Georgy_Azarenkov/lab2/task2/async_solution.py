import asyncio

import aiohttp
import httpx

from task2.database_connection import AsyncSession, Article
from task2.abstract_solution import AbstractSolution


class AsyncSolution(AbstractSolution):
    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self):
        tasks = self._aggregate_tasks_for_range(self._async_process_urls)
        await asyncio.gather(*tasks)

    async def _async_process_urls(self, urls):
        tasks = [self._async_process_single_url(url) for url in urls]
        await asyncio.gather(*tasks)

    async def _async_process_single_url(self, url):
        html_content = await self._async_load_html_content_from_url(url)
        title = self._sync_get_data_from_text_content(html_content)
        await self._async_save_to_db(url, title)

    async def _async_save_to_db(self, url, title):
        async with AsyncSession() as session:
            async with session.begin():
                article = Article(url=url, title=title)
                session.add(article)
                print(f'Статья сохранена: {article}')
                await session.commit()

    async def _async_load_html_content_from_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

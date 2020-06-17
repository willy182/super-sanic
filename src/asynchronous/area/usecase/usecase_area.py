import asyncio

from math import ceil

from configs.config import Config
from src.shared import usecase as uc
from src.shared.response import response_object as ro
from src.shared.response.response_object import CommonResponse
from src.asynchronous.area.serializers.area_serializers import AllAreaBaseSchema


class ListAllAreaUsecase(uc.UseCaseAsync):

    def __init__(self, repo):
        self.repo = repo

    async def process_request(self, request_objects):
        try:
            task1 = asyncio.create_task(self.repo.area.get_all_area(request_objects), name='data_area')
            task2 = asyncio.create_task(self.repo.area.get_total_area(request_objects), name='total_area')
            task3 = asyncio.create_task(self.repo.plankton.get_variant('/variants?noCache=true'), name='data_variant')
            task4 = asyncio.create_task(
                self.repo.plankton.get_variant('/variants?include=product,offers&page[number]=1&page[size]=100&filter[status]=published&channel=b2b&noCache=true'),
                name='plankton_include'
            )
            all_tasks = [task1, task2, task3, task4]
            done_tasks, pending_tasks = await asyncio.wait(all_tasks, return_when=asyncio.ALL_COMPLETED)

            for done in done_tasks:
                name = done.get_name()
                if name == 'data_area':
                    data = done.result()
                elif name == 'total_area':
                    total = done.result()
                elif name == 'data_variant':
                    data_plankton = done.result()
                elif name == 'plankton_include':
                    plankton_include = done.result()

            total_page = ceil(total / request_objects.limit)

            serializer_area = AllAreaBaseSchema().dump(data, many=True)

            plankton_tmp = []
            for i, row in enumerate(data_plankton.get('data')):
                if i == 3:
                    break
                else:
                    plankton_tmp.append(
                        {
                            'skuNo': row.get('skuNo'),
                            'fullname': row.get('fullname')
                        }
                    )

            for i, data in enumerate(serializer_area):
                if i == 11:
                    break
                else:
                    data['plankton'] = plankton_tmp

            response = {
                'success': True,
                'code': Config.STATUS_CODES[Config.SUCCESS],
                'message': Config.SUCCESS.lower(),
                'meta': {
                    'page': request_objects.page,
                    'limit': request_objects.limit,
                    'totalRecords': total,
                    'totalPages': total_page,
                },
                'data': serializer_area
            }

            return ro.ResponseSuccess(response)

        except asyncio.TimeoutError:
            return CommonResponse.build_common_message("time out error", Config.SYSTEM_ERROR)

        except Exception as e:
            return CommonResponse.build_common_message(str(e), Config.SYSTEM_ERROR)

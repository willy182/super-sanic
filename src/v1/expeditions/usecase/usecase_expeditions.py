import asyncio

from math import ceil

from configs.config import Config
from src.shared import usecase as uc
from src.shared.response import response_object as ro
from src.shared.response.response_object import CommonResponse
from src.v1.area.serializers.area_serializers import AreaBaseSchema
from src.v1.expeditions.serializers.expedition_serializers import ExpeditionBaseSchema


class ListExpeditionUsecase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    async def process_request(self, request_objects):
        try:
            task1 = asyncio.create_task(self.repo.expedition.get_all(request_objects))
            task2 = asyncio.create_task(self.repo.expedition.get_total(request_objects))
            task3 = asyncio.create_task(self.repo.area.get_subdistrict_by_zipcode(17111))
            task4 = asyncio.create_task(
                self.repo.plankton.get_variant('/variants?filter[skuNo]=3316920142&noCache=true')
            )
            all_tasks = [task1, task2, task3, task4]
            done_tasks, pending_tasks = await asyncio.wait(all_tasks, return_when=asyncio.ALL_COMPLETED)

            for done in done_tasks:
                name = done._coro.cr_code.co_name
                if name == 'get_all':
                    data_expedition = done.result()
                elif name == 'get_total':
                    data_total_expedition = done.result()
                elif name == 'get_subdistrict_by_zipcode':
                    data_area = done.result()
                elif name == 'get_variant':
                    data_plankton = done.result()

            total_page = ceil(data_total_expedition / request_objects.limit)

            serializer_expedition = ExpeditionBaseSchema().dump(data_expedition, many=True)
            serializer_area = AreaBaseSchema().dump(data_area, many=True)

            plankton_tmp = []
            for plankton in data_plankton.get('data'):
                plankton_tmp.append(
                    {
                        'skuNo': plankton.get('skuNo'),
                        'fullname': plankton.get('fullname')
                    }
                )

            for data in serializer_expedition:
                data['subDistrict'] = serializer_area
                data['plankton'] = plankton_tmp

            response = {
                'success': True,
                'code': Config.STATUS_CODES[Config.SUCCESS],
                'message': Config.SUCCESS.lower(),
                'meta': {
                    'page': request_objects.page,
                    'limit': request_objects.limit,
                    'totalRecords': data_total_expedition,
                    'totalPages': total_page,
                },
                'data': serializer_expedition
            }

            return ro.ResponseSuccess(response)

        except Exception as e:
            return CommonResponse.build_common_message(str(e), Config.SYSTEM_ERROR)

import asyncio

from math import ceil

from configs.config import Config
from src.shared import usecase as uc
from src.shared.response import response_object as ro
from src.shared.response.response_object import CommonResponse
from src.v1.area.serializers.area_serializers import AllAreaBaseSchema


class ListAllAreaUsecase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    async def process_request(self, request_objects):
        try:
            data = await asyncio.create_task(self.repo.area.get_all_area(request_objects))
            total = await asyncio.create_task(self.repo.area.get_total_subdistrict(request_objects))
            data_plankton = await asyncio.create_task(
                self.repo.plankton.get_variant('/variants?&noCache=true')
            )

            total_page = ceil(total / request_objects.limit)

            serializer_area = AllAreaBaseSchema().dump(data, many=True)

            plankton_tmp = []
            for i, row in enumerate(data_plankton.result().get('data')):
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

        except Exception as e:
            return CommonResponse.build_common_message(str(e), Config.SYSTEM_ERROR)

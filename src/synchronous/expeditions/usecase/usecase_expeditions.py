import asyncio

from math import ceil

from configs.config import Config
from src.shared import usecase as uc
from src.shared.response import response_object as ro
from src.shared.response.response_object import CommonResponse
from src.synchronous.area.serializers.area_serializers import AreaBaseSchema
from src.synchronous.expeditions.serializers.expedition_serializers import ExpeditionBaseSchema


class ListExpeditionUsecase(uc.UseCaseSync):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_objects):
        try:
            data_expedition = self.repo.expedition.get_all(request_objects)
            data_total_expedition = self.repo.expedition.get_total(request_objects)
            data_area = self.repo.area.get_subdistrict_by_zipcode(17111)
            data_plankton = self.repo.plankton.get_variant('/variants?filter[skuNo]=3316920142&noCache=true')

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

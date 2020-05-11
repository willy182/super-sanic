import asyncio

from configs.config import Config
from src.shared import usecase as uc
from src.shared.response import response_object as ro
from src.shared.response.response_object import CommonResponse
from src.v1.expeditions.serializers.expedition_serializers import ExpeditionBaseSchema


class ListExpeditionUsecase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    async def process_request(self, request_objects):
        try:
            data_expedition = await asyncio.create_task(self.repo.expedition.get_all(request_objects))
            data_area = await asyncio.create_task(self.repo.area.get_subdistrict_by_zipcode(17111))
            data_plankton = await asyncio.create_task(self.repo.plankton.get_variant('/variants?filter[skuNo]=3316920142'))

            # await data_expedition
            # await data_area
            # await data_plankton

            serializer = ExpeditionBaseSchema().dump(data_expedition, many=True)

            for data in serializer:
                data['subDistrict'] = data_area
                data['plankton'] = data_plankton

            return ro.ResponseSuccess(serializer)

        except Exception as e:
            return CommonResponse.build_common_message(str(e), Config.SYSTEM_ERROR)


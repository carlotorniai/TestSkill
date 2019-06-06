# coding: utf-8

from tapioca import TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin


from .resource_mapping import RESOURCE_MAPPING


class FifaApiClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    resource_mapping = RESOURCE_MAPPING

    def get_api_root(self, api_params, **kwargs):
        if api_params.get("mock"):
            return "http://www.mocky.io/v2/5cf825d8300000f7d4a38141"
        if api_params.get("qa"):
            return "https://api.qa.fifa.com/api/v1"
        return "https://api.fifa.com/api/v1"

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(FifaApiClientAdapter, self).get_request_kwargs(api_params, *args, **kwargs)

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs, response_data, response):
        pass


FifaApiWrapper = generate_wrapper_from_adapter(FifaApiClientAdapter)

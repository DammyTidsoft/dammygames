from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get("tags", None) or getattr(self.view, "tags", [])
        if not tags and operation_keys:
            tags = [operation_keys[0]]
        return tags

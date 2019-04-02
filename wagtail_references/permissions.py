from wagtail.core.permission_policies.collections import CollectionOwnershipPermissionPolicy
from references import get_reference_model
from references.models import Reference


permission_policy = CollectionOwnershipPermissionPolicy(
    get_reference_model(),
    auth_model=Reference,
    owner_field_name='created_by_user'
)

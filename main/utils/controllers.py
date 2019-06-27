from main.schemas.item import ItemSchema
from main.schemas.user import UserSchema


def item_with_user_information(item):
    item_detailed = ItemSchema(only=("id", "name", "description")).dump(item).data
    item_detailed["user"] = UserSchema(only=("id", "username")).dump(item.user).data
    return item_detailed


def item_with_user_and_date(item):
    item_detailed = ItemSchema(only=("id", "name", "description", "created", "updated")).dump(item).data
    item_detailed["user"] = UserSchema(only=("id", "username")).dump(item.user).data
    return item_detailed


def items_with_user_information(items):
    items_detailed = [item_with_user_information(item) for item in items]
    return items_detailed

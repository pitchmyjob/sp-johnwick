from .shared_task import shared_task


@shared_task
def test(ok, user):
    print("test ===>", user)
    print("test == >", ok)

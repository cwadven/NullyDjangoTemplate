from django.db import migrations


def forward(apps, schema_editor):
    ProductType = apps.get_model('product', 'ProductType')
    ProductItemInfoType = apps.get_model('product', 'ProductItemInfoType')

    # ProductType 생성
    ProductType.objects.create(
        id=1,
        name='의류',
        sequence=1,
    )
    ProductType.objects.create(
        id=2,
        name='기타',
        sequence=2,
    )

    # ProductItemInfoType 생성
    ProductItemInfoType.objects.create(
        id=1,
        name='색상',
        sequence=2,
    )
    ProductItemInfoType.objects.create(
        id=2,
        name='사이즈',
        sequence=2,
    )
    ProductItemInfoType.objects.create(
        id=3,
        name='디자인',
        sequence=3,
    )
    ProductItemInfoType.objects.create(
        id=4,
        name='기타',
        sequence=3,
    )


def backward(apps, schema_editor):
    ProductType = apps.get_model('product', 'ProductType')
    ProductItemInfoType = apps.get_model('product', 'ProductItemInfoType')

    # ProductType
    ProductType.objects.filter(
        id__in=[1, 2]
    ).delete()

    # ProductItemInfoType
    ProductItemInfoType.objects.filter(
        id__in=[1, 2, 3]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]

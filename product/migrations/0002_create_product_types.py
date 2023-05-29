from django.db import migrations


def forward(apps, schema_editor):
    ProductType = apps.get_model('product', 'ProductType')
    InfoType = apps.get_model('product', 'InfoType')

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

    # InfoType 생성
    InfoType.objects.create(
        id=1,
        name='색상',
    )
    InfoType.objects.create(
        id=2,
        name='사이즈',
    )
    InfoType.objects.create(
        id=3,
        name='디자인',
    )
    InfoType.objects.create(
        id=4,
        name='기타',
    )


def backward(apps, schema_editor):
    ProductType = apps.get_model('product', 'ProductType')
    InfoType = apps.get_model('product', 'InfoType')

    # ProductType
    ProductType.objects.filter(
        id__in=[1, 2]
    ).delete()

    # InfoType
    InfoType.objects.filter(
        id__in=[1, 2, 3]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iati_codelists', '0002_auto_20170704_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityscope',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='activitystatus',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='aidtypeflag',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='budgetidentifier',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='budgetidentifiersector',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='budgetidentifiersectorcategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='budgetstatus',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='budgettype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='collaborationtype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='conditiontype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='contacttype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='descriptiontype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='documentcategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='documentcategorycategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='fileformat',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='financetypecategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='flowtype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='gazetteeragency',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='geographicalprecision',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='geographicexactness',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='geographiclocationreach',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='humanitarianscopetype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='indicatormeasure',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='loanrepaymentperiod',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='loanrepaymenttype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='locationtype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='locationtypecategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='organisationidentifier',
            name='name',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='organisationregistrationagency',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='organisationrole',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='organisationtype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='otherflags',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='otheridentifiertype',
            name='name',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='policysignificance',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='publishertype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='relatedactivitytype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='resulttype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='sector',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='sectorcategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='tiedstatus',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='transactiontype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='valuetype',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='verificationstatus',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='version',
            name='name',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class GspOwnerShipStatus(models.Model):

    """
        This class is used to define corresponding HQ Owner and lgsi domain ownership status for each
        Google security patch.
    """

    GSP_OwnerShip_Status = models.CharField(max_length=128)

    def __str__(self):
        return self.GSP_OwnerShip_Status

    class Meta:
        verbose_name_plural = "GSP_OwnerShip_Status"


class HQDomainOwner(models.Model):

    """
        This class is used to define the HQ owner attribute for corresponding LGSI Domain owner.
    """

    HQ_Domain_Owner = models.CharField(max_length=128)

    def __str__(self):
        return self.HQ_Domain_Owner

    class Meta:
        verbose_name_plural = "HQ_Domain_Owners"


class LGSIDomainOwner(models.Model):

    """
        This class is used to define the lgsi Owner attribute for each Google security patch.
        This is an intermediatory model associated with ManytoManyField using the through argument
        to point to the model that will act as an intermediary.
    """

    LGSI_Domain_Owner = models.CharField(max_length=128)

    def __str__(self):
        return self.LGSI_Domain_Owner

    class Meta:
        verbose_name_plural = "LGSI_Domain_Owners"


class Category(models.Model):

    """
        This class is used to define the category of each Google security patch.
    """

    category = models.CharField(max_length=128)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Categories"


class GSP(models.Model):

    """
        By default ,Django gives each model the following field,an Automatic primary Key
        id = models.AutoField(primary_key=True)

        If You would like to specify custom primary key,just specify primary_key = true on one of your fields
        If Django sees you have explicitly set Field.primary_key it won't add the automatic id column.

        Each field type,except for ForeignKey,ManytoManyField,OneToOneField takes an optional first
        positional argument a verbose name.If verbose name is not given then Django will automatically
        create it using fields attribute name ,converting underscores to spaces.

        In case of FKey, ManytoManyField and OneToOneField Use the first argument to be a model class,so use
        the verbose_name keyword argument.

        This class is used to define the attributes for adding google security patch
    """

    GSP_Category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="the GSP category")
    Security_Patch_level = models.CharField(max_length=128)
    Applicability = models.CharField(max_length=128)
    Description = models.URLField(max_length=128)
    LGSIDomainOwners = models.ManyToManyField(LGSIDomainOwner)
    HQDomainOwners = models.ManyToManyField(HQDomainOwner)
    OwnersShipStatus = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Google Security Patches"

    def __str__(self):
        return self.Description
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wilgis
"""
import arcpy
from datetime import date
import os


class BackupQGis():
    def __init__(self, caminho_pasta):
        self.caminho = caminho_pasta
        self.mxd = arcpy.mapping.MapDocument("Current")
        self.lyr = arcpy.mapping.ListLayers(self.mxd)

    '''- A função abaixo cria as pastas e subpastas onde serão inseridos
       os shapefiles de backup.
       - A primeria pasta a ser criada é nomeada com a data de criação.
       - As subpastas criadas são criadas nomeadas com números
       de vezes que foi feito o backup.
    '''
    def criar_pasta(self):
        self.data_hoje = date.today()
        self.dia = self.data_hoje.day
        self.mes = self.data_hoje.month
        self.ano = self.data_hoje.year
        self.data = str(self.dia)+'_'+str(self.mes)+'_'+str(self.ano)
        self.nova_pasta = self.caminho + self.data
        if os.path.exists(self.nova_pasta):
            self.lista_pasta = os.listdir(self.nova_pasta)
            if self.lista_pasta == []:
                num = '01'
                self.nova_pasta = self.nova_pasta + '\\' + num
                os.mkdir(self.nova_pasta)
            else:
                lista_pasta_2 = []
                for i in self.lista_pasta:
                    nome_pasta_existe = int(i)
                    lista_pasta_2.append(nome_pasta_existe)
                lista_pasta_2.sort()
                num = lista_pasta_2[-1] + 1
                nome_pasta = '0' + str(num)
                self.nova_pasta = self.nova_pasta + '\\' + str(nome_pasta)
                os.mkdir(self.nova_pasta)
        else:
            num = '01'
            os.mkdir(self.nova_pasta)
            self.nova_pasta = self.nova_pasta + '\\' + num
            os.mkdir(self.nova_pasta)
            
    ''' - A função abaixo cria os shapefiles de backups
    na pasta criada acima.'''
    def criar_backup(self):
        self.lista_layers = []
        for i in range(len(self.lyr)):
            desc = arcpy.Describe(self.lyr[i].name)
            try:
                desc.shapeType
                self.lista_layers.append(self.lyr[i].name)
            except AttributeError:
                pass
        arcpy.FeatureClassToShapefile_conversion(self.lista_layers,
                                                 self.nova_pasta)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:49:48 2019

@author: Luikigaba
"""

import numpy as np
import os
from sentinelhub import BBox, CRS, DataSource,get_area_info, AwsTile, AwsTileRequest
import time
import pyproj
import pandas as pd
import shutil

os.chdir('/Volumes/Transcend/Sentinel')

def extractpoints(band,highreselem,points):
    ratio = highreselem/band.shape[0]
    
    values = []
    for element in points:
        a = int(np.floor(element/highreselem))
        b = int(element-np.floor(element/highreselem)*highreselem)
        
        values.append(band[int(np.floor(a/ratio)),int(np.floor(b/ratio))])
    
    return(values)
    
def coordinatematrix(tile_info,highreselem,EPSG,n_bins): #Función que procesa la información del tile para obtener coordenadas de cada pixel + lonid/latid
    
    #tile_info -> Variable que incluye toda la información sobre el tile
    #highreselem -> Número de elementos que tiene la banda con más resolución de la imagen
    #EPSG -> Sistema de coordenadas en el que están expresadas las coordenadas del tile
    #n_bins -> Número de metros por bin para lonid y latid
    
    EPSGtile = pyproj.Proj("+init=EPSG:"+EPSG) 
    EPSGWGS84 = pyproj.Proj("+init=EPSG:4326") #Almacena las proyecciones a realizar
    
    x1tile=tile_info['tileGeometry']['coordinates'][0][0][0]
    x2tile=tile_info['tileGeometry']['coordinates'][0][1][0]
    y1tile=tile_info['tileGeometry']['coordinates'][0][0][1]
    y2tile=tile_info['tileGeometry']['coordinates'][0][2][1] #Almacena las coordenadas de las esquinas del tile
    
    
    coordsxhigh=np.linspace(x1tile,x2tile,highreselem+1,dtype='uint32')
    coordsxhigh=coordsxhigh+5
    coordsxhigh=np.delete(coordsxhigh,coordsxhigh.shape[0]-1)
    
    coordsyhigh=np.linspace(y1tile,y2tile,highreselem+1,dtype='uint32')
    coordsyhigh=coordsyhigh-5
    coordsyhigh=np.delete(coordsyhigh,coordsyhigh.shape[0]-1)
    
    #Ya se tienen las coordenadas X e Y del punto medio de cada pixel de la imagen
    
    lon, lat = pyproj.transform(EPSGtile, EPSGWGS84, coordsxhigh, coordsyhigh) #Conversión de las coordenadas X e Y a WGS84
    
    binningCoef=np.round((2*np.pi*6371000)/(360*n_bins),2) 
    
    lonid=binningCoef*np.multiply(lon,np.cos(2*np.pi*lat/360))
    lonid=lonid.astype('int')
    
    latid=binningCoef*lat
    latid=latid.astype('int')
    
    #Ya se han obtenido las claves primarias de la base de datos: lonid y latid
    
    coordmatx,coordmaty=np.meshgrid(lon,lat)
    lonidmat,latidmat=np.meshgrid(lonid,latid)
    
    coordmatx=coordmatx.flatten()
    coordmaty=coordmaty.flatten()
    latidmat=latidmat.flatten()
    lonidmat=lonidmat.flatten()
    
    return coordmatx,coordmaty,latidmat,lonidmat


if __name__ == "__main__":
    INSTANCE_ID = ''  # In case you put instance ID into cofniguration file you can leave this unchanged
    
    search_bbox = BBox(bbox=[-3.71,40.42,-3.688,40.40], crs=CRS.WGS84)
    search_time_interval = ('2015-03-01T00:00:00', '2019-03-20T23:59:59')
    n_bins = 10
    
    points = pd.read_csv("pixelcentromad.csv",header=None).iloc[:,1].to_list()
    
    infos = get_area_info(search_bbox, search_time_interval, maxcc=0.10)
        
    for i in range(10,len(infos)):
        
            errort = 0
            
            element = infos[i]
            
            dictibanda = dict()
            
            fecha = element['properties']['startDate']
            dictibanda['Fecha'] = [fecha]*len(points)
            dictibanda['Torre'] = [x for x in range(24)]
            dictibanda['Cloud'] = [element['properties']['cloudCover']]*len(points)
            
            aux = element['properties']['productIdentifier']
        
            tile_name, time, aws_index = AwsTile.tile_id_to_tile(aux)
        
            bands = ['R10m/B02', 'R10m/B03', 'R10m/B04', 'R10m/B08', 'R20m/B05',
                     'R20m/B06', 'R20m/B07', 'R20m/B11', 'R20m/B12', 'R60m/B01',
                     'R60m/B09']
        
            for banda in bands:
                metafiles = ['tileInfo']
        
                data_folder = './AwsData'
                
                try:
                    request = AwsTileRequest(tile=tile_name, time=time, aws_index=aws_index,
                                             bands=banda, metafiles=metafiles, data_folder=data_folder,
                                             data_source=DataSource.SENTINEL2_L2A)
                except:
                    errort = 1
                    print('Salto')
                    break
        
                request.save_data()
        
                try:
                    bandita,tileinfo = request.get_data()
                except:
                    errort = 2
                    print('Salto')
                    break
                
                EPSG=tileinfo['tileOrigin']['crs']['properties']['name'].split(':')[-1]
                highreselem = 10980
                
                values = extractpoints(bandita,highreselem,points)
                
                dictibanda[banda] = values
                
                print(banda)
                
            if errort == 1:
                continue
            
            if errort == 2:
                papa = time.split('-')
            
                if len(papa[1])==1:
                    papa[1] = str(0)+papa[1]
    
                if len(papa[2])==1:
                    papa[2] = str(0)+papa[2]
    
                foldername = tile_name+','+'-'.join(papa)+','+str(aws_index)
                    
                shutil.rmtree("AwsData/"+foldername, ignore_errors=False, onerror=None)
                
                continue
            
            pd.DataFrame.from_dict(dictibanda).to_csv('H4G/'+str(i)+'.csv',index=False)
            
            papa = time.split('-')
            
            if len(papa[1])==1:
                papa[1] = str(0)+papa[1]

            if len(papa[2])==1:
                papa[2] = str(0)+papa[2]

            foldername = tile_name+','+'-'.join(papa)+','+str(aws_index)
                
            shutil.rmtree("AwsData/"+foldername, ignore_errors=False, onerror=None)
            
            print(i)
        
        
        
        
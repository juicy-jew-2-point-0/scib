#!/usr/bin/env python
# coding: utf-8

import scanpy as sc
import scIB
import warnings
warnings.filterwarnings('ignore')

def runIntegration(inPath, outPath, method, hvg, batch):

    adata = sc.read(inPath)

    if hvg:
        adata = scIB.preprocessing.hvg_intersect(adata, batch, adataOut=True)

    integrated_tmp = scIB.metrics.measureTM(method, adata, batch)

    integrated = integrated_tmp[2][0]


    integrated.uns['mem'] = integrated_tmp[0]
    integrated.uns['runtime'] = integrated_tmp[1]

    sc.write(outPath, integrated)

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run the integration methods')

    parser.add_argument('-m', '--method', required=True)
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    parser.add_argument('-b', '--batch', required=True, help='Batch variable')
    parser.add_argument('-v', '--hvgs', help='Preselect for HVGs', action='store_true')

    args = parser.parse_args()
    file = args.input_file
    out = args.output_file
    batch = args.batch
    hvg = args.hvgs
    method = args.method
    methods = {
        'scanorama': scIB.integration.runScanorama,
        'scgen': scIB.integration.runScGen,
        'seurat': scIB.integration.runSeurat,
        'harmony': scIB.integration.runHarmony,
        'mnn': scIB.integration.runMNN,
        'bbknn': scIB.integration.runBBKNN,
        'conos': scIB.integration.runConos
    }
    
    if method not in methods.keys():
        raise ValueError('Method does not exist. Please use one of the following:\n'+str(list(methods.keys())))
    
    run= methods[method]
    runIntegration(file, out, run, hvg, batch)
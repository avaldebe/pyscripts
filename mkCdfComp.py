#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as cdf
import os

#------------------ arguments  ----------------------------------------------

parser=argparse.ArgumentParser()
parser.add_argument('-k','--varkeys',nargs='*',help='varname  string in nc file, can be partial eg ug_PM')
parser.add_argument('-i','--ifiles',help='Input files',nargs='*',required=True)
parser.add_argument('-d','--domain',help='domain wanted, i0 i1 j0 j1, e.g. "30 100 40 80"',required=True)
parser.add_argument('-p','--plot',help='plot on screen?',action='store_true')
parser.add_argument('-s','--suffix',help='suffix if not Base/Base_month.nc?',required=False)
parser.add_argument('-v','--verbose',help='extra info',action='store_true')
parser.add_argument('-y','--year',help='year',required=True)
args=parser.parse_args()
dtxt='CdfComp'
dbg=False
if args.verbose: dbg=True
if dbg: print(dtxt+'ARGS', args)

i0, i1, j0, j1 = [ int(i) for i in args.domain.split() ]
print(dtxt+' domain', i0, i1, j0, j1 )

case=dict()
cases=[]
ifiles=[]
for ifile in args.ifiles:
   #print('TRY ', ifile)
   #print('TRY ', ifile.split('/') )
   if args.suffix:
      f = ifile + '/' + suffix  # Adds, NOT TESTED YET
   else:
      f = ifile + '/Base/Base_month.nc'  # Default
   
   case[f]= f.split('/')[-3].replace('.%s'%args.year,'')  # rv4.2012 from rv4.2012/Base/Base_month.nc
   cases.append(case[f])
   ifiles.append(f)  # with full path name to .nc
   print(dtxt+'CASE', case[f] )

#suffix='.2012/Base/Base_month.nc'

first=True
file0=ifiles[0] #  + cases[0] + suffix # Need file to get keys at start
print('F0', file0)

ecdf=cdf.Dataset(file0,'r',format='NETCDF4')
keys = ecdf.variables.keys()
tab=open('ResCdfCompTab_%s.txt' % '_'.join(cases), 'w' )
header='%-30s' % 'Variable'
for c in cases: 
  header += ( '%18s' % c )
tab.write('%s\n' %  header )
for var in args.varkeys:
   if dbg: print(' VAR ', var )
   for key in keys:
       if dbg: print(' VAR, KEY ', var, key )
       if not var in key:
           continue

       tab.write('%-30s' % key)
       print('Processing ', var, key )

       for ifile in ifiles: 

           ecdf=cdf.Dataset(ifile,'r',format='NETCDF4')
           if key in ecdf.variables.keys():
             vals=ecdf.variables[key][:,j0:j1+1,i0:i1+1]
             monthly = np.mean(vals,axis=(1,2))
           else:
             print(' KEY NOT FOUND ', key, case[ifile])
             monthly = np.full(12,np.nan)
           plt.plot(monthly,label=case[ifile])
           tab.write('%18.3f' % np.mean(monthly) )
           if dbg: print('M:', monthly)

       plt.title(key)
       plt.ylim(ymin=0.0)
       plt.legend()
       plt.savefig('PlotCdfComp_%s_%s.png' % ( key, '_'.join(cases) ))
       if args.plot: 
         plt.show()
       #plt.clf()
       plt.close()
       tab.write('\n')

#
#veg=bcdf.variables['FstO3_IAM_CR'][0,:,:] # Land-mask?
#
##base = veg[j0:j1+1, i0:i1+1]
##test = veg[j0:j1+1, i0:i1+1]
#
##plt.imshow(veg2)
##plt.show()
##print( i0, i1, j0, j1, lats[j0], lats[j1], np.mean(veg[j0:j1+1, i0:i1+1]), np.mean(veg2) )
#
#var='CR'
#n=np.zeros([2,24])
#v=np.zeros([2,24])
#for ivar in range(2):
#  o3=hcdf.variables['CanopyO3_IAM_%s' % var ][:,j0:j1+1,i0:i1+1]
#  print( 'Starting ', var, np.max(o3), np.mean(o3) )
#  o3t=o3[:,0,0]
#  o3j=o3[0,:,0]
#  o3i=o3[0,0,:]
#  h=1
#  for k in range(len(o3t)):
#   #mask == veg2 > 0.0
#    for j in range(len(o3j)):
#      for i in range(len(o3i)):
#        if veg2[j,i] > 0.0:
#          v[ivar,h] += np.mean( o3[k,:,:] )
#          n[ivar,h] += 1
#    h += 1
#    if h == 24: h = 0
#  v[ivar,:] /= n[ivar,:] 
#  meanv = np.mean( v[ivar,:] )
#  v[ivar,:] /= meanv
#  var='DF'  # reset for next ivar
#
#with open('Results_HourlyTable.txt','w') as f:
#  f.write( '%2s  %8s  %8s\n' % ( 'h', 'Crop', 'Tree' ))
#  for h in range(24):
#     f.write( '%2.2d  %8.3f  %8.3f\n' %  ( h, v[0,h], v[1,h] ) )
#
#plt.plot(v[0,:],label='crops')
#plt.plot(v[1,:],label='forest')
#plt.legend()
#plt.savefig('Hourly5deg.png')
#plt.show()
##print('RES n ', i, n )
##print('RES v ', i, v/n )
#
#

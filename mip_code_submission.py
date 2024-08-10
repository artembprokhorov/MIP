from gurobipy import Model, GRB, LinExpr, QuadExpr
import pandas as pd
import gurobipy
import numpy as np
import numpy.matlib
import os.path


import os
import sys

PATH_OUT1 = 'res_regr_500_output/'
PATH_IN = '/blue/username/username/one_break/'

# def solve_MIP(df1, B, L, C, st_I=None, st_A=None):
    
#     np.random.seed(15)
#     T = len(df1)
#     model_mip = Model('Regr2')
#     model_mip.Params.TIME_LIMIT = 450.0
#     model_mip.Params.Threads = 1
#     if C != 0:
#         model_mip.Params.Cutoff = C#+0.0001
#     model_mip.Params.OutputFlag = 0
#     a = {}
#     z = {}
#     y = {}
#     d = {}
#     M = 5 #20
#     #L = 15
#     l = 0.8

#     #b = model_mip.addVar(vtype=GRB.INTEGER)

#     #f = model_mip.addVar(vtype=GRB.CONTINUOUS)

#     int_mark = {}

#     for i in range(T-1):
#         int_mark[i] = model_mip.addVar(vtype=GRB.BINARY)
#         if st_I is not None:
#             int_mark[i].Start = st_I[i]
        
#     for j in range(T):
#         #y[j] = model_mip.addVar(vtype=GRB.BINARY)

#         for i in range(1):
#             a[j,i] = model_mip.addVar(vtype=GRB.CONTINUOUS, lb=-5, ub=5)
#             #z[j,i] = model_mip.addVar(vtype=GRB.BINARY)
#             if st_I is not None:
#                 a[j,i].Start = st_A[j]


#     for i in range(T-1):
#         for j in range(1):
#             model_mip.addConstr(a[i+1,j] - a[i,j] <=  M*int_mark[i])
#             model_mip.addConstr(a[i+1,j] - a[i,j] >= -M*int_mark[i])


#     # less N
#     model_mip.addConstr(sum([int_mark[i] for i in int_mark ]) == B)
    
#     for i in range(T-2):
#         model_mip.addConstr(int_mark[i] + int_mark[i+1] <= 1)

#     expr_obj = QuadExpr(0)
#     #expr_obj = LinExpr(0)
#     for i,j in df1.head(T).iterrows():
#         expr_obj.add((j['y'] - a[i,0]*j['X1']) * (j['y'] - a[i,0]*j['X1']))
#         #expr_obj.add((j['y'] - a[i,0]*j['X1'] - a[i,1]*j['X2'] - a[i,2]*j['X3'] - a[i,3]))

#     #expr_obj.add( L* sum([int_mark[i] for i in int_mark ] ))  
#     expr_obj.add(L*(B))
#     model_mip.update()
#     model_mip.setObjective(expr_obj, GRB.MINIMIZE)
#     model_mip.optimize()
#     st_i, st_a = None, None
#     try:
#         st_i = [int_mark[i].X for i in range(len(int_mark))]
#         st_a = [a[i, 0].X for i in range(len(a))]
#     except:
#         pass
#     return model_mip.ObjVal, st_i, st_a


print('running',sys.argv[1])
fname = open('params/param_%s'%sys.argv[1]) #sys.argv[1]
for line in fname:
    
    problem_file = line.strip()
    print(line)
    if os.path.isfile('completed_problems/%s'%problem_file.replace(' ','_')):
        print(problem_file, 'exists')
        continue

    
    t = line.strip().split(" ")
    fn = t[0]
    col_id = t[1]
    
    df = pd.read_csv(PATH_IN+'%s'%fn)
    df = df[['x_%s'%col_id,'y_%s'%col_id]]
    df.columns = ['X1','y']
    
    T = len(df)
    df1 = df
    
    
    Lambda_Max = 'N/A'
    steps = 'N/A'
    sti, sta = None, None
    #LS = np.logspace(np.log10(0.01*Lambda_Max),np.log10(Lambda_Max),10)
    for lmbd_ind, lmbd_param in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
        model_mip = Model('Regr2')
        model_mip.Params.TIME_LIMIT = 450.0
        model_mip.Params.Threads = 1
        model_mip.Params.LogToConsole = 0
        model_mip.Params.LogFile = 'gur_logs/log_'+fn[:-4]+'_'+str(col_id)+'_'+str(lmbd_ind)+'.txt'
        print('start with br %s'%lmbd_param)
        #print(sti, sta)
        a = {}
        z = {}
        y = {}
        d = {}
        M = 5 #20

        int_mark = {}

        for i in range(T-1):
            int_mark[i] = model_mip.addVar(vtype=GRB.BINARY)
            if sti is not None:
                int_mark[i].Start = sti[i]

        for j in range(T):
            #y[j] = model_mip.addVar(vtype=GRB.BINARY)

            for i in range(1):
                a[j,i] = model_mip.addVar(vtype=GRB.CONTINUOUS, lb=-5, ub=5)
                #z[j,i] = model_mip.addVar(vtype=GRB.BINARY)
                if sta is not None:
                    a[j,i].Start = sta[j]


        for i in range(T-1):
            for j in range(1):
                model_mip.addConstr(a[i+1,j] - a[i,j] <=  M*int_mark[i])
                model_mip.addConstr(a[i+1,j] - a[i,j] >= -M*int_mark[i])

                #model_mip.addConstr(a[i+1,j] - a[i,j] >=  l*(int_mark[i]) - d[i,j]*40)
                #model_mip.addConstr(a[i+1,j] - a[i,j] <=  -l*(int_mark[i]) + (1-d[i,j])*40 )   
        '''
        for i in range(200-1):
            for j in range(1):
                #model_mip.addConstr(a[i+1,j] - a[i,j] <=  L*int_mark[i])
                #model_mip.addConstr(a[i+1,j] - a[i,j] >= - L*int_mark[i])

                model_mip.addConstr(a[i+1,j] - a[i,j] >=  l*(int_mark[i]) - d[i,j]*40)
                model_mip.addConstr(a[i+1,j] - a[i,j] <=  -l*(int_mark[i]) + (1-d[i,j])*40 )   
        '''
        # less N
        model_mip.addConstr(sum([int_mark[i] for i in int_mark ]) == lmbd_param)
        
        
        for i in range(T-2):
            model_mip.addConstr(int_mark[i] + int_mark[i+1] <= 1)

        expr_obj = QuadExpr(0)
        #expr_obj = LinExpr(0)
        for i,j in df1.head(T).iterrows():
            expr_obj.add((j['y'] - a[i,0]*j['X1']) * (j['y'] - a[i,0]*j['X1']))
            #expr_obj.add((j['y'] - a[i,0]*j['X1'] - a[i,1]*j['X2'] - a[i,2]*j['X3'] - a[i,3]))

        #expr_obj.add( lmbd_param* sum([int_mark[i] for i in int_mark ] ))  #removed 13 June
        
        
        
        model_mip.update()
        model_mip.setObjective(expr_obj, GRB.MINIMIZE)
        model_mip.optimize()
        
        A = [a[i].X for i in a if i[1] == 0]
        #B = [a[i].X for i in a if i[1] == 1]
        I = [-100]+[int_mark[i].X for i in int_mark]
        
        sti, sta = None, None
        try:
            sti = [int_mark[i].X for i in range(len(int_mark))]
            sta = [a[i, 0].X for i in range(len(a))]
        except:
            print("no sol!")
        
        curr_res = pd.DataFrame()
        curr_res['a1'] = A
        curr_res['a2'] = -1
        curr_res['int_mark'] = I
        cfn = PATH_OUT1+'res_'+fn[:-4]+'_'+str(col_id)+'_'+str(lmbd_ind)
        curr_res.to_csv(cfn+'.csv')
        fres = open(PATH_OUT1+'params_'+fn[:-4]+'_'+str(col_id)+'_'+str(lmbd_ind)+'.txt','w')
        fres.write("%s"%model_mip.status)
        fres.write("\n")
        fres.write("%s"%model_mip.ObjVal)
        fres.write("\n")
        fres.write("%s"%model_mip.Runtime)
        fres.write("\n")
        fres.write("%s"%lmbd_param)
        fres.write("\n")
        fres.write("%s"%Lambda_Max)
        fres.write("\n")
        fres.write("%s\n"%steps)
        fres.write("%s\n"%model_mip.MIPGap)
        fres.close() 
        print("%s complete"%lmbd_ind)
    f = open('completed_problems/%s'%problem_file.replace(' ','_'),'w')
    f.write(' ')
    f.close()


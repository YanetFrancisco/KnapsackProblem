__author__ = 'Yanet_Francisco_Suárez'

import random

class Utils:

    def __init__(self):
        self.nodos=[]
        self.solucion={}
        self.optimo=-(2**32)
        self.optimo_genetico=-(2**32)
        self.solucion_gentico=[]
        self.g=0

    def estandarizando(self,is_max,fo,rest,termInd):
        variables=[]
        datos={}
        z=0
        #if self.comparar_vector_con_0(termInd)
        if not is_max:
            for x in range(len(fo)):
                fo[x] *= -1
        for x in range(len(fo)):
            if fo[x]>0:
                variables.append(x)
                z+=fo[x]
                fo[x] *= -1
        for x in rest:
            for y in variables:
                rest[x][y]*=-1
                termInd[x]+=rest[x][y]
        datos['z']=z
        datos['fo']=fo
        datos['variables']=variables
        datos['rest']=rest
        datos['termInd']=termInd
        return datos,variables

    def algoritmo_balas(self,datos):
       #Inicializando
        vl=[] # conjunto de variables libres
        for x in range(len(datos['fo'])):
            vl.append(x) # inicialmente todas las variable son libres
            self.nodos.append(False)
            self.optimo=-(2**32) # valor optimo
        actual=0 # valor actual
        w0=[] # conjunto de la variables fijadas en 1
        w1=[] # conjunto de las variables fijadas en 0
        self.auxiliar(vl,w0,w1,datos['termInd'],datos['rest'],0,datos['fo'])
        return self.optimo,self.solucion

    def auxiliar(self,vl,w0,w1,termInd, rest, k,fo):
       print('w1:')
       print(w1)
       print('w0:')
       print(w0)
       print('variables libres:')
       print(vl)
       actual= self.valor_actual_fo(w1=w1,fo=fo)
       if actual>=self.optimo:
           s=self.calculo_s(termInd=termInd,rest=rest,w1=w1)
           if self.comparar_vector_con_0(s):
               self.optimo=actual
               for x in range(len(w1)):
                    self.solucion[x]=w1[x]
                    print('solucion actual:')
               for x in self.solucion:
                    print(self.solucion[x],":1")
               print('optimo actual:')
               print(self.optimo)
               return
           t = self.calculo_t(rest=rest,vl=vl)
           q= self.calculo_q(s=s)
           if self.comparar_vectores(s=s,t=t,q=q):
               return
           else:
               r=self.calculo_r(q=q,rest=rest,vl=vl)
               i=self.calculo_i(r=r,rest=rest,s=s)
               #if not self.nodos[i]:
               vl.remove(i)
               w1.append(i)
               self.auxiliar(vl=vl,w0=w0,w1=w1,termInd=termInd,rest=rest,k=k,fo=fo)
               w1.remove(i)
               w0.append(i)
               self.auxiliar(vl=vl,w0=w0,w1=w1,termInd=termInd,rest=rest,k=k,fo=fo)
               #self.nodos[i]=True
               w0.remove(i)
               vl.append(i)

    def mayor(self):
        self.nodos.reverse()
        for x in range(len(self.nodos)):
            if not self.nodos[x]:
                return len(self.nodos)-(x+1)

    def calculo_i(self,r,rest,s):
        resp={}
        menor_valor=2**16
        var=0
        for j in r:
            aux=0
            for i in rest:
                aux+= max(rest[i][j]-s[i],0)
            resp[j]=aux
            if aux < menor_valor:
                menor_valor=aux
                var=j
        return var

    def calculo_t(self,rest,vl):
        t=[]
        for i in rest:
            aux=0
            for j in vl:
                aux+= min(rest[i][j],0)
            t.append(aux)
        return t

    def calculo_r(self,q,rest,vl):
        r=[] #variables que tienen coef <0 de las rest de q y que pert a vl
        for y in q:
            for x in range(len(rest[y])):
                if vl.__contains__(x) and not r.__contains__(x) and rest[y][x]<0 :
                    r.append(x)
        return r

    def calculo_q(self,s):
         q=[] #restricciones que son <0
         for x in range(len(s)):
             if s[x]<0 : q.append(x)
         return q

    def calculo_s(self,termInd,rest,w1):
        s=[]
        if len(w1)==0: return termInd
        for r in range(len(termInd)):
            aux=0
            for v in w1:
                aux+=rest[r][v]
            s.append(termInd[r]-aux)
        return s

    def valor_actual_fo(self,w1,fo):
        actual=0
        for x in w1:
            actual+=fo[x]
        return actual

    def comparar_vector_con_0(self,a):
        for x in a:
            if x<0: return False
        return True

    def resta_vectores(self,s,b):
        aux=[]
        for x in range(len(s)):
            aux.append(b[x]-s[x])
        return aux

    def comparar_vectores(self,s,t,q):
        for x in q:
            if t[x]>s[x]: return True
        return False

    def mochila_alg(self,datos,condicion,pesoMax):
        if condicion==0:
            aux=[]
            for x in range(len(datos[0])):
                aux.append((datos[0][x],datos[1][x],x))
            print("Valores:")
            print(aux)
            mochila=self.algoritmo_voraz(pesoMax,aux)
        elif condicion==1:
            aux=[]
            for x in range(len(datos[0])):
                aux.append((datos[1][x],datos[1][x],x))
            print("Valores:")
            print(aux)
            mochila=self.algoritmo_voraz(pesoMax,aux)
        elif condicion==2:
            aux=[]
            for x in range(len(datos[0])):
                aux.append((datos[2][x],datos[1][x],x))
            print("Valores:")
            print(aux)
            mochila=self.algoritmo_voraz(pesoMax,aux)
        sol=0
        for x in range(len(fo)):
            if x in mochila:
                sol+=datos[0][x]
        return mochila,sol

    def algoritmo_voraz(self,pesoMax,aux):
        mochila=[]
        #almacen.sort(reverse=True)
        aux.sort(key=lambda y: y[0],reverse=True)
        print('Elementos ordenados:')
        print(aux)
        pesoM=0
        posicion=0
        while pesoM<pesoMax and posicion<len(aux):
            print('Probando con:')
            print(aux[posicion])
            tmp=aux[posicion][1]
            if pesoM+tmp<=pesoMax:
                print('Valido')
                mochila.append(aux[posicion][2])
                pesoM+=tmp
            posicion+=1
        return mochila

    def algoritmo_genetico(self,cant_ind, cant_var,fo,rest,c, cant_gen,tipo_seleccion,tipo_emparejamiento,tipo_cruzamiento):
        pob=self. generar_poblacion(cant_ind,cant_var,c,rest)
        while cant_gen!=0:
            print('---------------------------------')
            print('Generacion :%d '% cant_gen)
            eval=self.eval_pob(pob,fo,c)
            print('Evaluacion:')
            print(eval)
            pro= self.pro_pob(eval)
            print('Salud:')
            print(pro)
            sel= self.seleccion(pro,tipo_seleccion)
            print('Seleccion:')
            print(sel)
            parejas=self.emparejamiento(pro,sel,tipo_emparejamiento)
            print('Parejas:')
            print(parejas)
            nueva_poblacion= self.cruzamiento(pob,parejas,tipo_cruzamiento,cant_var)
            print('Nueva Poblacion despues de Cruzamiento:')
            print(nueva_poblacion)
            nueva_poblacion=self.mutacion(nueva_poblacion,cant_var,c,rest)
            print('Nueva Poblacion despues de Mutacion:')
            print(nueva_poblacion)
            pob=nueva_poblacion
            cant_gen-=1
        return self.optimo_genetico,self.solucion_gentico,self.g

    def generar_poblacion(self, cant_ind, cant_var,c,rest):
        pob=[]
        import random
        aux=0
        while aux<cant_ind:
            r= random.randint(0,(2**cant_var)-1)
            tmp=self.int_to_binary(r,cant_var)
            if not tmp in pob and self.es_factible(tmp,c,rest):
                pob.append(tmp)
                aux+=1
        return pob

    def es_factible(self,ind,c,rest):
        aux=0
        for x in range(len(rest)):
            aux+= rest[x]*ind[x]
            if aux>c : return False
        return True

    def int_to_binary(self,n,cant_var):
        b=[]
        count=0
        while n!=0:
            b.append(n%2)
            n = int(n/2)
            count+=1
        while count<cant_var:
            b.append(0)
            count+=1
        b.reverse()
        return b

    def pro_pob(self,eval):
        pro={}
        total=0
        for x in eval.keys():
            total+=eval[x]
        for x in eval.keys():
            pro[x]=eval[x]/total
        return pro

    def seleccion(self,pro,tipo_seleccion):
        aux=[]
        for x in pro.keys():
            aux.append((pro[x],x))
        aux.sort(key=lambda y: y[0],reverse=True)
        if tipo_seleccion==0:
            sel=self.ruleta(aux)
        elif tipo_seleccion==1:
            sel=self.todos_un_hijo(aux)
        return sel

    def ruleta(self, pro):
        cant_ind=len(pro)
        sel={}
        for x in range(cant_ind):
            sel[x]=0
        count=0
        while count<cant_ind:
            r=random.random()
            n=self.dime_quien_es(r,pro)
            if n!=-1:
                sel[n]+=1
            count+=1
        return sel

    def dime_quien_es(self,r,pro):
        tmp=0
        for x in pro:
            tmp+=x[0]
            if r<=tmp:
                return x[1]
        return -1

    def todos_un_hijo(self,pro):
        sel={}
        count=0
        for x in range(len(pro)):
            sel[count]=1
            count+=1
        return sel

    def emparejamiento(self,pro,sel,tipo_emparejamiento):
        if tipo_emparejamiento==0:
            return self.por_orden(pro)
        elif tipo_emparejamiento==1:
            return self.por_ruleta(pro,sel)

    def por_orden(self,pro):
        parejas=[]
        aux=[]
        for x in pro.keys():
            aux.append((pro[x],x))
        aux.sort(key=lambda y: y[0],reverse=True)
        for x in range(0,len(aux),2):
            parejas.append((aux[x][1],aux[x+1][1]))
        return parejas

    def por_ruleta(self,pro,sel):
        parejas=[]
        tanque=[]
        for x in sel.keys():
            if sel[x]!=0 and not x in tanque:
                tanque.append(x)
        count=0
        while count<len(pro):
            r=random.choice(tanque)
            while sel[r]<=0:
                r=random.choice(tanque)
            r2=random.choice(tanque)
            while sel[r2]<=0 or (r2==r and sel[r2]<=1):
                r2=random.choice(tanque)
            parejas.append((r,r2))
            sel[r]-=1
            sel[r2]-=1
            count+=2
        return parejas

    def cruzamiento(self, pob,parejas, tipo_cruzamiento,cant_var):
        if tipo_cruzamiento==0:
            return self.cruzamiento_simple(pob,parejas,cant_var)
        elif tipo_cruzamiento==1:
            return self.cruzamiento_uniforme(pob,parejas,cant_var)

    def cruzamiento_simple(self,pob,parejas,cant_var):
        import random
        r =random.randint(0,cant_var-1)
        nueva_pob=[]
        for x in parejas:
            padre= pob[x[0]]
            madre=pob[x[1]]
            hija=[]
            hijo=[]
            for y in range(0,r+1):
                hija.append(padre[y])
                hijo.append(madre[y])
            for z in range(r+1,cant_var):
                hija.append(madre[z])
                hijo.append(padre[z])
            nueva_pob.append(hija)
            nueva_pob.append(hijo)
        return nueva_pob

    def cruzamiento_uniforme(self,pob,parejas,cant_var):
        nueva_pob=[]
        r=random.getrandbits(cant_var)
        mask= self.int_to_binary(r,cant_var)
        not_mask=[]
        for x in mask:
            not_mask.append(1-x)
        for x in parejas:
            padre=pob[x[0]]
            madre=pob[x[1]]
            hijo= self.operador(padre,mask,True)
            hija= self.operador(madre,not_mask,False)
            nueva_pob.append(hijo)
            nueva_pob.append(hija)
        return nueva_pob

    def operador(self,padre,mask,cond):
        hijo=[]
        for x in range(len(padre)):
            if padre[x]==mask[x] and cond: hijo.append(1)
            elif padre[x]==mask[x] and not cond: hijo.append(0)
            elif padre[x]!=mask[x] and cond: hijo.append(0)
            elif padre[x]!=mask[x] and not cond: hijo.append(1)
        return hijo

    def mutacion(self, nueva_pob,cant_var,c, rest):
        import random
        r =random.randint(0,cant_var-1)
        r2=random.randint(0,len(nueva_pob)-1)
        if nueva_pob[r2][r]==0:
            nueva_pob[r2][r]=1
        else: nueva_pob[r2][r]=0
        for x in nueva_pob:
            while not self.es_factible(x,c,rest):
                r =random.randint(0,cant_var-1)
                #r2=random.randint(0,len(nueva_pob)-1)
                if x[r]==0:
                    x[r]=1
                else: x[r]=0
        return nueva_pob

    def eval_pob(self,pob,fo,c):
        eval={}
        for x in range(len(pob)):
            #tmp=0
            z=0
            for y in range(len(pob[x])):
                #tmp+=rest[y]*pob[x][y]
                z+=fo[y]*pob[x][y]
            #if tmp<=c:
            if z>self.optimo_genetico:
                self.optimo_genetico=z
                self.solucion_gentico=pob[x]
                self.g+=1
            eval[x]=z
            #else:
                #z -= k * (tmp - c)
                #eval[x]=(tmp,z)
        return eval



#Testing

rest={}
#rest[0]=[-5,-7,-10,-3,-1]

#rest[0]= [-3,-2]
#rest[1]=[-1,1]

#rest[0]=[7,2,2]
#rest[1]=[2,-3,-5]
#rest[2]=[8,-1,-4]

#rest[0]=[125,50,500,25]
rest=[30,20,22,10,7]


#rest[0]=[-1,3,-5,-1,4]
#rest[1]=[2,-6,3,2,-2]
#rest[2]=[0,1,-2,1,1]

#rest[0]=[-1,3,-5,-1,4]
#rest[1]=[2,-6,3,-5,-1]
#rest[2]=[0,1,-2,1,1]

#termInd=[-2,0,-1]
#termInd=[-4,0]

#termInd=[3,-2,-3]

#termInd=[575]
#fo=[3000,100,6000,30]

termInd=[40]
fo=[100,75,80,40,20]

#fo=[-2,-9,-1]

#fo=[-1,-3]
#fo=[-5,-7,-10,-3,-1]
#datos={}
#datos['rest']=rest
#datos['termInd']=termInd
#datos['fo']=fo
#a= Utils()
#print("solucion")
#datos= a.estandarizando(True,fo=fo, termInd=termInd,rest=rest)
#a.algoritmo_balas(datos=datos)
#a.mochila_alg({0:[100,75,80,40,20],1:[30,20,22,10,7],2:[100/30,75/20,80/22,40/10,20/7]},0,40)
#print('con el valor')
#a.mochila_alg({0:[100,75,80,40,20],1:[30,20,22,10,7],2:[100/30,75/20,80/22,40/10,20/7]},1,40)
#print('con el peso')
#a.mochila_alg({0:[100,75,80,40,20],1:[30,20,22,10,7],2:[100/30,75/20,80/22,40/10,20/7]},1,40)
#print('con el valor/peso')
#print("end solucion")
#vl=[0,1,2,3,4]
#s=calculo_s(termInd,rest,[])
#q=calculo_q(s)
#t=calculo_t(rest,vl)
#r= calculo_r(q,rest)
#i=calculo_i(r,rest,s)
#print(min(rest[2]))
#print(q)
#print(t)
#print(r)
#print(i)


#a.algoritmo_genetico(4,5,fo,rest,40,5,1,1,0)
#print(a.optimo_genetico)
#print(a.solucion_gentico)



#aux = a.seleccion(pro)
#a.ruleta(aux)


#print(Utils.algoritmo_balas(termInd=termInd,fo=rest[0],rest=rest))
#fo=[-5,7,10,3,1]
#variables=[]
#z=0
#for x in range(len(fo)):
#    fo[x] *= -1
#    if fo[x]>0:
#        variables.append(x)
#        z+=fo[x]
#        fo[x] *= -1
#print('variables',variables)
#print('fo',fo)
#print('z',z)
#
#for x in rest:
#    print(rest[x])


class beam():

    def __init__(self,height,width,length):

        # Mechanical Values
        self.height = height
        self.width = width
        self.length = length
        self.weight = 0

        # Numerical Settings
        
        self.d = 0.001
        self.sub_div_plot = 4
        self.x_axis = [i*self.d for i in range(int(self.length/self.d))]
        self.n = len(self.x_axis)

        # Loads and reactions
        self.id = 0
        self.load_list = []
        self.support_list = []
        self.shear_list = []
        self.moment_list = []

        # References
        self.reference = 'https://en.wikipedia.org/wiki/Beam_(structure)'
    
    def LagrangePolynomial(self,x_list,y_list):

        if len(x_list) != len(y_list):
            print('Error: x_list e y_list have a different lenghts')
            return 0
        else:
            len_xy_list = len(x_list)
            polynomial = '0'

            for i in range(len_xy_list):
                
                numerator = '1'
                denominator = '1'
                for j in range(len_xy_list):
                    if i != j:
                        numerator = numerator + f'*(x - {x_list[j]})'
                        denominator = denominator + f'*({x_list[i]} - {x_list[j]})'
                    else:
                        pass

                polynomial = polynomial + f'+(({y_list[i]}) * (({numerator[2:]}) / ({denominator[2:]})))'

            degree = i
            analytic_polynomial = polynomial[2:]
            polynomial_function = lambda x: eval(analytic_polynomial)
            
            return polynomial_function
    
    def Simpson_3_8_Sum(self,function,a,b,n=1e6):
    
        first_step_fractional = 1/3
        second_step_fractional = 2/3

        SS38 = 0
        h = (b - a) / n
        sub_div = 3
        xk_1 = a
        i_max = int(n)


        for i in range(i_max):

            # xk_1: inicio do intervalo
            # xk: fim do intervalo
            # xki: xk_1 + primeira fração (geralmente 1/3) do intervalo
            # xkj: xk_1 + segunda fração (geralmente 2/3) do intervalo

            xk_1 = a + (i*h)
            xk = xk_1 + h
            xki = xk_1 + (h*first_step_fractional)
            xkj = xk_1 + (h*second_step_fractional)
            SS38 = SS38 + (((function(xk_1) + (3*function(xki)) + (3*function(xkj)) + function(xk))*h*3)/(sub_div*8))

        return SS38
    
    def moment(self,load_function,left,right):
        moment_value = []
        for i in self.x_axis:
            if i < left:
                moment_value.append(0)
            elif i <= right and i >= left:
                load_temporary = self.Simpson_3_8_Sum(load_function,left,i,n=1)
                if load_temporary == 0:
                    moment_value.append(0)
                else:
                    lever_arm_temporary = (i - (self.Simpson_3_8_Sum(lambda x:load_function(x)*x,left,i,n=1))/load_temporary)
                    moment_value.append(load_temporary*lever_arm_temporary)
            elif i > right:
                load_temporary = self.Simpson_3_8_Sum(load_function,left,right,n=1)
                lever_arm_temporary = (i - (self.Simpson_3_8_Sum(lambda x:load_function(x)*x,left,right,n=1))/load_temporary)
                moment_value.append(load_temporary*lever_arm_temporary)
            else:
                moment_value.append(0)
        return moment_value

    def shear(self,load_function,left,right):
        shear_value = []
        for i in self.x_axis:
            if i < left:
                shear_value.append(0)
            elif i <= right and i >= left:
                shear_value.append(self.Simpson_3_8_Sum(load_function,left,i,n=1))
            elif i > right:
                shear_value.append(self.Simpson_3_8_Sum(load_function,left,right,n=1))
            else:
                shear_value.append(0)
        return shear_value

    def add_point_support(self,x, support_value, support_type):
        self.id = self.id + 1
        s = lambda:support_value
        x0 = x - self.d
        x1 = x + self.d
        support_info = {
            'id':self.id,
            'left':x0,
            'right':x1,
            'support_type':support_type,
            'support_function':s
                        }
        support_info['support_point'] = [s() if i <= x1 and i >= x0 else 0 for i in self.x_axis]
        support_info['shear_point'] = [s() if i >= x1 or i >= x0 else 0 for i in self.x_axis]
        # Not Work
        support_info['moment_point'] = [s()*(i - x0) if i >= x1 or i >= x0 else 0 for i in self.x_axis]
        self.support_list.append(support_info)

    def add_point_load(self,x,load_value):
        self.id = self.id + 1
        pl = lambda:load_value
        x0 = x - self.d
        x1 = x + self.d
        load_info = {
            'id':self.id,
            'left':x0,
            'right':x1,
            'load_function':pl
                     }
        load_info['load_point'] = [pl() if i <= x1 and i >= x0 else 0 for i in self.x_axis]
        load_info['shear_point'] = [pl() if i >= x1 or i >= x0 else 0 for i in self.x_axis]
        # Not Work
        load_info['moment_point'] = [pl()*(i - x0) if i >= x1 or i >= x0 else 0 for i in self.x_axis]
        self.load_list.append(load_info)

    def add_distributed_load(self,x,load_value):
        self.id = self.id + 1
        degree = len(x)
        dl = self.LagrangePolynomial(x,load_value)
        x0 = x[0]
        x1 = x[-1]
        load_info = {
            'id':self.id,
            'left':x0,
            'right':x1,
            'load_function':dl
                     }
        load_info['load_point'] = [dl(i) if i <= x1 and i >= x0 else 0 for i in self.x_axis]
        load_info['shear_point'] = self.shear(dl,x0,x1)
        load_info['moment_point'] = self.moment(dl,x0,x1)
        self.load_list.append(load_info)
    
    def check(self):
        pass
    
    def update(self):
        # Shear
        shear_total = [0 for i in self.x_axis]
        for i in self.support_list:
            for j in range(self.n):
                shear_total[j] = shear_total[j] + i['shear_point'][j]
        for i in self.load_list:
            for j in range(self.n):
                shear_total[j] = shear_total[j] + i['shear_point'][j]
        self.shear_list = shear_total
        moment_total = [0 for i in self.x_axis]

        # Moment
        for i in self.support_list:
            for j in range(self.n):
                moment_total[j] = moment_total[j] + i['moment_point'][j]
        for i in self.load_list:
            for j in range(self.n):
                moment_total[j] = moment_total[j] + i['moment_point'][j]
        self.moment_list = moment_total

    # Diagrams
    # support_draw not work
    def support_draw(x,y,b,h,support_type):
        if support_type == 1:
            color = 'fuchsia'
            name = 'roller'
        elif support_type == 2:
            color = 'deeppink'
            name = 'hinged'
        elif support_type == 3:
            color = 'orchid'
            name = 'fixed'
        else:
            color = 'purple'
            name = 'undefined'

        plt.plot([x,x-b,x+b,x],[y,y-h,y-h,y],c=color,label=name)
        plt.plot([x-(1.5*b),x+(1.5*b)], [y-h,y-h],c=color)
        for i in range(-1,10):
            plt.plot([x-b + 0.5 + (i*0.5),x-b + (i*0.5)],[y-h - 0.5,y-h],c=color)

    def plot_moment(self):
        self.update()
        plt.figure(figsize=(18,3), dpi=100)

        # Bending Moment
        plt.plot([0]+self.x_axis, [0]+self.moment_list, c='red',label='bending moment')
        y_max_moment = max(self.moment_list)
        x_max_moment = self.x_axis[self.moment_list.index(y_max_moment)]
        y_min_moment = min(self.moment_list)
        x_min_moment = self.x_axis[self.moment_list.index(y_min_moment)]
        plt.plot([x_max_moment,x_max_moment], [0,y_max_moment], c='lime',label=f'max moment = ({round(x_max_moment,3)} m, {round(y_max_moment,3)} kNm)')
        plt.scatter([x_max_moment,x_max_moment], [0,y_max_moment], c='lime')
        plt.plot([x_min_moment,x_min_moment], [0,y_min_moment], c='springgreen',label=f'min moment = ({round(x_min_moment,3)} m, {round(y_min_moment,3)} kNm)')
        plt.scatter([x_min_moment,x_min_moment], [0,y_min_moment], c='springgreen')
        
        # Beam
        plt.plot([0,self.length,self.length,0,0], [0,0,-self.height,-self.height,0],c='black')
        
        # Settings
        plt.xlabel('Length Beam (m)')
        plt.ylabel('Bending Moment (kNm)')
        plt.title('Bending Moment Diagram')
        plt.legend()
        plt.grid(linestyle='--', linewidth=0.5)
        plt.xticks([i/self.sub_div_plot for i in range(int(self.sub_div_plot*self.length+1))])
        plt.ylim(max([0]+self.moment_list)+10,(min([0]+self.moment_list) - self.height)-10)
        plt.show()

    def plot_shear(self):
        self.update()
        plt.figure(figsize=(18,3), dpi=100)

        # Shear Force
        plt.plot([0]+self.x_axis, [0]+self.shear_list, c='red',label='shear force')
        
        # Beam
        plt.plot([0,self.length,self.length,0,0], [0,0,-self.height,-self.height,0],c='black')
        
        # Settings
        plt.xlabel('Length Beam (m)')
        plt.ylabel('Shear Force (kN)')
        plt.title('Shear Force Diagram')
        plt.legend()
        plt.grid(linestyle='--', linewidth=0.5)
        plt.xticks([i/self.sub_div_plot for i in range(int(self.sub_div_plot*self.length+1))])
        plt.show()

    def plot_load(self):
        plt.figure(figsize=(18,3), dpi=100)

        load_total = [0 for i in self.x_axis]
        support_total = [0 for i in self.x_axis]
        
        # Supports
        for i in self.support_list:
            for j in range(self.n):
                support_total[j] = support_total[j] + ((-1)*(i['support_point'][j]))
        
        
        plt.plot([0]+self.x_axis+[self.length], [0]+support_total+[0], c='blue',label='support')
        
        # Loads
        for i in self.load_list:
            for j in range(self.n):
                load_total[j] = load_total[j] + ((-1)*(i['load_point'][j]))
        
        plt.plot([0]+self.x_axis+[self.length], [0]+load_total+[0], c='red',label='load')
        
        # Beam
        plt.plot([0,self.length,self.length,0,0], [0,0,-self.height,-self.height,0],c='black')
        
        # Settings
        plt.xlabel('Length Beam (m)')
        plt.ylabel('Load (kN)')
        plt.title('Load Diagram')
        plt.legend()
        plt.grid(linestyle='--', linewidth=0.5)
        plt.xticks([i/self.sub_div_plot for i in range(int(self.sub_div_plot*self.length+1))])
        plt.show()
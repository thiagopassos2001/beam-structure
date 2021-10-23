import matplotlib.pyplot as plt

class beam():

    def __init__(self,height,width,length):
        self.height = height
        self.width = width
        self.length = length
        self.weight = 0
        self.d = 0.001
        self.x_axis = [i*self.d for i in range(int(self.length/self.d))]
        self.n = len(self.x_axis)
        self.load_list = []
        self.support_list = []
        self.id = 0
        self.reference = 'https://en.wikipedia.org/wiki/Beam_(structure)'
        self.shear_list = []
        self.moment_list = []
    
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
    
    def shear(self,load_function,left,right):
        shear_value = []
        
        for i in self.x_axis:
            if i < left:
                shear_value.append(0)
            elif i <= right and i >= left:
                shear_value.append(((load_function(left) + load_function(i))*(i - left)*0.5))
            elif i > right:
                shear_value.append(((load_function(left) + load_function(right))*(right - left)*0.5))
            else:
                shear_value.append(0)
        
        return shear_value

    def add_support(self,x, support_value, support_type):
        self.id = self.id + 1
        s = lambda x:support_value
        x0 = x - self.d
        x1 = x + self.d
        support_info = {
            'id':self.id,
            'left':x0,
            'right':x1,
            'support_function':s
                        }
        support_info['support_point'] = [s(i) if i <= x1 and i >= x0 else 0 for i in self.x_axis]
        support_info['shear_point'] = [s(i) if i >= x1 or i >= x0 else 0 for i in self.x_axis]

        self.support_list.append(support_info)

    def add_point_load(self,x,load_value):
        self.id = self.id + 1
        pl = lambda x:load_value
        # Not Work
        # dpl = lambda x:load_value*x
        x0 = x - self.d
        x1 = x + self.d
        load_info = {
            'id':self.id,
            'left':x0,
            'right':x1,
            'load_function':pl
                     }
        load_info['load_point'] = [pl(i) if i <= x1 and i >= x0 else 0 for i in self.x_axis]
        load_info['shear_point'] = [pl(i) if i >= x1 or i >= x0 else 0 for i in self.x_axis]
        # Not Work
        # load_info['moment_point'] = [dpl(i) if i >= x1 or i >= x0 else 0 for i in self.x_axis]

        self.load_list.append(load_info)

    def add_distributed_load(self,x,load_value):
        self.id = self.id + 1
        degree = len(x)
        dl = self.LagrangePolynomial(x,load_value)
        # Not Work
        #ddl = self.LagrangePolynomial(self.x_axis[::int(self.n/100)], [dl(j) for j in self.x_axis[::int(self.n/100)]])
        #dl = lambda x:load_value0 + (((load_value1-load_value0)/(x1-x0))*(x0+x))
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
        # Not Work
        # load_info['moment_point'] = self.shear(ddl,x0,x1)

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

    # Diagrams
    # Not Work
    '''def plot_moment(self):
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
        plt.xticks([i/2 for i in range(int(2*self.length+1))])
        plt.show()'''

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
        plt.xticks([i/2 for i in range(int(2*self.length+1))])
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
        plt.xticks([i/2 for i in range(int(2*self.length+1))])
        plt.show()
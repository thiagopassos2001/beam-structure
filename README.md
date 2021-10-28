# Viga (Estrutura) (Beam (Structure))
Classe para calcular numericamente cargas, esforços cortantes e momento fletor, gerando diagramas pelo matplotlib.

* **REPOSITÓRIO INCOMPLETO**
## Exemplo de Código
~~~python

v1 = beam(0.5,0.25,15)
v1.add_point_support(0,67.5139,1)
v1.add_point_support(12,96.4861,2)
v1.add_distributed_load([0,7],[-10,-10])
v1.add_distributed_load([6,13],[-5,-15])
v1.add_point_load(6,-17)
v1.add_point_load(15,-7)
~~~

~~~python
v1.sub_div_plot = 2
v1.update()
v1.plot_load()
v1.plot_shear()
v1.plot_moment()
~~~

* Diagrama de Cargas (Load Diagram)
![image](https://user-images.githubusercontent.com/71474825/139163957-f71a43f9-57b3-4a71-a95a-a77374d11e77.png)
* Diagrama de Força Cortante (Shear Force Diagram)
![image](https://user-images.githubusercontent.com/71474825/139164016-4be784cb-4eec-4ee3-97c2-354f3b677124.png)
* Diagrama de Momento Fletor (Bending Moment Diagram)
* ![image](https://user-images.githubusercontent.com/71474825/139164073-14e8e59e-ed77-43f1-b0d6-3501e0545e84.png)

# Viga (Estrutura) (Beam (Structure))
Classe para calcular numericamente cargas, esforços cortantes e momento fletor, gerando diagramas pelo matplotlib.

* **REPOSITÓRIO INCOMPLETO**
## Exemplo de Código
~~~python

v1 = beam('V1',0.5,0.25,3.0) # Create a beam
v1.add_point_support(0,15,1) # Create a punctual support
v1.add_point_support(3,15,2) # Create a punctual support
v1.add_distributed_load([0,3],[-10,-10]) # Create a distributed load
v1.sub_div_plot = 2 # Set a division x axis values
~~~

* Resumo das Informações da Viga
~~~python
v1.info_beam()
~~~

~~~python
Property		Value		Unity
--------------------------------------------------
Informations
Name:			V1
Height:			0.5		(m)
Width:			0.25		(m)
Length:			3.0		(m)
Weight:			0		(kg)
--------------------------------------------------
Loads and Supports
Number of Loads:	1		-
Number of Supports:	2		-
--------------------------------------------------
Shear Force
Maximum Value:		0.0, 15.0	(m, kN)
Minumum Value:		2.998, -14.98	(m, kN)
Null Value*:		1.5, 0.0	(m, kN)
--------------------------------------------------
Bending Moment
Maximum Value:		1.5, 11.265	(m, kNm)
Minumum Value:		0.0, 0.015	(m, kNm)
Null Value*:		0.0, 0.015	(m, kNm)
--------------------------------------------------
*There may be more null values
~~~

* Diagrama de Cargas (Load Diagram)
~~~python
v1.plot_load()
~~~
![image](https://user-images.githubusercontent.com/71474825/139559309-eb527146-4331-4006-8446-aca19c58de0a.png)
* Diagrama de Força Cortante (Shear Force Diagram)
~~~python
v1.plot_shear()
~~~
![image](https://user-images.githubusercontent.com/71474825/139559312-0045f0f8-bbdd-4d9f-9717-d0c234fe50f7.png)
* Diagrama de Momento Fletor (Bending Moment Diagram)
~~~python
v1.plot_moment()
~~~
![image](https://user-images.githubusercontent.com/71474825/139559314-2867f6a3-b120-44cd-8ec0-e66679a4cee3.png)

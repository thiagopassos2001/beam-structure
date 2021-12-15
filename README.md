# Viga (Estrutura) (Beam (Structure))
Classe para calcular numericamente cargas, esforços cortantes e momento fletor por meio a da sobreposição do efeito das cargas e a discretização em pontos ao longo do comprimento da viga. Utiliza matplotlib para a geração dos diagramas. Inspirado em softwares como o Ftool (https://www.ftool.com.br/) e Viga Online (https://www.aprenderengenharia.com.br/viga-online).

Ferramentas:
* Esforços Cortantes em um ponto qualquer ao longo do comprimento discretizado
* Momentos Fletores em um ponto qualquer ao longo do comprimento discretizado

## Exemplo de Código
~~~python

# Create a beam
v1 = beam('V1',0.5,0.25,6)

# Loads and Moments

# Create a pure bending moment
# 32 kNm value at the moment
# Apply in 4 m
v1.add_pure_bending_moment(4,32)

# Create a distributed load
# Beginning with 15 kN/m and ending with 5kN/m
# Start at 0 m and end at 4 m
v1.add_distributed_load([0,6],[-15,-5])

# Create a punctual force
# 10 kN value at the force
# Apply in 1 m
v1.add_point_load(1, -10)
# 15 kN value at the force
# Apply in 2.5 m
v1.add_point_load(2.5, -15)

# Supports

# 43.625 kN value at the force
# Apply in 0 m
# 2 support gender
v1.add_point_support(0,43.625,2) # Create a punctual support

# 41.375 kN value at the force
# Apply in 4 m
# 1 support gender
v1.add_point_support(4,41.375,1) # Create a punctual support

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
Length:			6		(m)
Weight:			0		(kg)
--------------------------------------------------
Loads and Supports
Number of Loads:	3		-
Number of Supports:	2		-
--------------------------------------------------
Shear Force
Maximum Value*:		0.0, 43.625	(m, kN)
Minumum Value*:		4.0, -28.04	(m, kN)
Null Value*:		6.0, 0.001	(m, kN)
--------------------------------------------------
Bending Moment
Maximum Value*:		2.5, 51.531	(m, kNm)
Minumum Value*:		4.0, -12.218	(m, kNm)
Null Value*:		5.936, -0.004	(m, kNm)
--------------------------------------------------
*There may be more values
~~~

* Diagrama de Cargas (Load Diagram)
~~~python
v1.plot_load()
~~~

Resultado do script:
![image](https://user-images.githubusercontent.com/71474825/145699411-95df3f59-215d-434c-8dc7-2f97d0ae6c27.png)

* Diagrama de Força Cortante (Shear Force Diagram)
~~~python
v1.plot_shear()
~~~

Resultado do script:
![image](https://user-images.githubusercontent.com/71474825/146239589-b2713701-010e-46af-9dba-d9c9e4569088.png)

* Diagrama de Momento Fletor (Bending Moment Diagram)
~~~python
v1.plot_moment()
~~~

Resultado do script:
![image](https://user-images.githubusercontent.com/71474825/146239619-289d99c8-7aa6-4ce2-9ad7-cc059f620fa6.png)

a_array={
        '1':0,
         ' ':0.03,
         'ц':0.12,
         'и':0.21,
        'т':0.3,
        'г':0.39,
        'р':0.48,
        'а':0.57,
        'н':0.66,
        'е':0.83}
b_array={
         '1':0.03,
         ' ':0.12,
         'ц':0.21,
        'и':0.3,
        'т':0.39,
        'г':0.48,
        'р':0.57,
        'а':0.66,
        'н':0.83,
        'е':1}
#c_array=[0,0.03,0.12,0.21,0.3,0.39,0.48,0.57,0.66,0.83,1]
#c_array=[0,0.2,0.4,0.6,0.8,1]
'''
L_array=[0 for i in range(len(c_array))]
h_array=[1 for i in range(len(c_array))]

for i in range(1,len(c_array),1):
    L_array[i]=L_array[i-1]+c_array[-i-1]*(h_array[i-1]-L_array[i-1])
    h_array[i]=L_array[i-1]+c_array[-i]*(h_array[i-1]-L_array[i-1])
    #print(L_array[i])

for i in range(len(c_array)):
    print(i, L_array[i], h_array[i])
'''
string = 'аргентинец ценит негра1'
L_array=[0 for i in range(len(string))]
h_array=[1 for i in range(len(string))]

for i in range(1,len(string),1):
    L_array[i]=L_array[i-1]+a_array[string[i]]*(h_array[i-1]-L_array[i-1])
    h_array[i]=L_array[i-1]+b_array[string[i]]*(h_array[i-1]-L_array[i-1])

for i in range(len(string)):
    print(i, L_array[i], h_array[i])
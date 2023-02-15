import numpy as np
import matplotlib.pyplot as plt

#This function gives the tight lower bound of the TV distance.
def calc_LB_TVD(mp, sp, mq, sq):
    a = mp - mq
    return a**2 / ((sp+sq)**2 + a**2)

#This function gives the tight lower bound of the squared Hellinger distance.
def calc_LB_Hellinger(mp, sp, mq, sq):
    a = mp - mq
    return 1 - (sp+sq) * np.sqrt(1 / ((sp+sq)**2 + a**2))

def calc_mean_std(prob, x_array):
    mean = np.sum(prob * x_array)
    sigma = np.sqrt(np.sum(prob * x_array**2) - mean**2)
    return mean, sigma

def calc_prob(rand_array):
    return rand_array / np.sum(rand_array)
    
num_points = 5  # Number of elements in the set where two distribution are defined.  
trial_num = 10000 # Number of trials.
mode = 'TV' # 'TV': TV distance, 'HE': Hellinger distance.

result_list = []
LB_list = []

for i in range(trial_num):
    print(i)
    x_array = np.random.rand(num_points) 
    rand_array_p = np.random.rand(num_points)
    rand_array_q = np.random.rand(num_points)
    prob_p = calc_prob(rand_array_p)
    prob_q = calc_prob(rand_array_q)
    
    mp, sp = calc_mean_std(prob_p, x_array)
    mq, sq = calc_mean_std(prob_q, x_array)
    
    mp2, sp2 = calc_mean_std(prob_p, (x_array - 0.5) ** 5)
    mq2, sq2 = calc_mean_std(prob_q, (x_array - 0.5) ** 5)
    
    mp3, sp3 = calc_mean_std(prob_p, (x_array - 0.5) ** 10)
    mq3, sq3= calc_mean_std(prob_q, (x_array - 0.5) ** 10)
    
    if mode == 'TV':
         tv = 0.5 * np.sum(np.abs(prob_p - prob_q)) # TV distance
         LB_TVD = max(calc_LB_TVD(mp, sp, mq, sq), calc_LB_TVD(mp2, sp2, mq2, sq2), calc_LB_TVD(mp3, sp3, mq3, sq3))
         #LB_TVD = calc_LB_TVD(mp, sp, mq, sq)
         result_list.append(tv)
         LB_list.append(LB_TVD)
         plt.title('Comparison of TV distance with Lower bound')
         plt.xlabel('TV distance')
    elif mode == 'HE':
        h = 1.0 - np.sum(np.sqrt(prob_p * prob_q)) # Squared Hellinger distance
        LB_H = max(calc_LB_Hellinger(mp, sp, mq, sq), calc_LB_Hellinger(mp2, sp2, mq2, sq2), calc_LB_Hellinger(mp3, sp3, mq3, sq3))
        result_list.append(h)
        LB_list.append(LB_H)
        plt.title('Comparison of square Hellinger distance with Lower bound')
        plt.xlabel('Hellinger distance')
    else:
        print('Not implemented.')
        
x = np.arange(0.0, 1.0, 0.01)
y = np.arange(0.0, 1.0, 0.01)
plt.plot(x, y, color="red", linestyle='--', label='Bound')      
plt.plot(result_list, LB_list, 'o', color='none', markersize=5, markeredgewidth=1, markeredgecolor='blue', label='Result') 
plt.legend()
plt.show()       
    
    
    
    
    
   
    
    
   


#plt.plot(result_TV_list , LB_TV_list, 'o') 



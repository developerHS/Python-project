#정렬

##########버블정렬##########
def bubble_sort(array):
     compare=0
     change=0
    
     for i in range(len(array)-1):
         for j in range(len(array)-1):
             if (array[j]>array[j+1]):
                 change += 1
                 buffer = array[j]
                 array[j] = array[j+1]
                 array[j+1] = buffer
             compare += 1
     print(array)

     return array;
##########선택정렬##########
def selection_sort(array):
     compare=0
     change=0
    
     for i in range(len(array)-1):
         pivot = i
         for j in range(i, len(array)-1):
             if (array[pivot]>=array[j+1]):
                 pivot += 1
             compare += 1
         change += 1
         buffer = array[i]
         array[i] = array[pivot]
         array[pivot] = buffer
         compare += 1
     print(array)

     return array;



selection_sort([5,3,1,2,4])
    

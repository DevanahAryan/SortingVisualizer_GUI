from math import fabs
from os import curdir
import pygame
import random
pygame.init()

FPS=60

class DrawInformation:
    BLACK=0,0,0
    WHITE=255,255,255
    RED=255,0,0
    GREEN=0,255,0
    GREY=128,128,128
    BACKGROUND_COLOR=WHITE
    SIDE_PAD=100
    TOP_PAD=150
    FONT=pygame.font.SysFont("comicans",30)
    LARGE_FONT=pygame.font.SysFont("comicans",50)
    GRADIENTS=[
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]
    def __init__(self,width,height,lst):
        self.width=width
        self.height=height
        self.window=pygame.display.set_mode((width,height))
        pygame.display.set_caption("\t Sorting Visualiser!!")
        self.set_lst(lst)
    
    def set_lst(self,lst):
        self.lst=lst
        self.min_val=min(lst)
        self.max_val=max(lst)

        self.block_width=round((self.width-self.SIDE_PAD)/len(lst))
        self.block_height=round((self.height-self.TOP_PAD)/(self.max_val-self.min_val+1))
        self.start_x=self.SIDE_PAD//2

def draw_lst(draw_info,j=-1,k=-1,sorting=False):
    lst=draw_info.lst
    if sorting:
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR,(draw_info.SIDE_PAD//2,draw_info.TOP_PAD,draw_info.width-draw_info.SIDE_PAD,draw_info.height-draw_info.TOP_PAD))

    for i,val in enumerate(lst):
        x=draw_info.start_x+i*draw_info.block_width
        y=draw_info.height-((val-draw_info.min_val)*draw_info.block_height)
        if i==j:
            color=draw_info.GREEN
        elif i==k:
            color=draw_info.RED
        else:
            color=draw_info.GRADIENTS[i%3]
        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width,draw_info.height-y))


    if sorting==True:
        pygame.display.update()
    

def draw(draw_info,sorting_algo,ascending=True):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    if  ascending:
        # print(sorting_algo)
        GUIDE_ALGO=draw_info.FONT.render(f"{sorting_algo} - Ascending",1,draw_info.GREEN)
        draw_info.window.blit(GUIDE_ALGO,(draw_info.width/2-GUIDE_ALGO.get_width()/2,10))
    elif  not ascending:
        GUIDE_ALGO=draw_info.FONT.render(f"{sorting_algo} - Descending",1,draw_info.GREEN)
        draw_info.window.blit(GUIDE_ALGO,(draw_info.width/2-GUIDE_ALGO.get_width()/2,10))
    GUIDE=draw_info.FONT.render("R - Reset | Space - Start Sorting | A - Ascending | D - Descending",1,(0,0,0))
    draw_info.window.blit(GUIDE,(draw_info.width/2-GUIDE.get_width()/2,40+10))
    GUIDE_B=draw_info.FONT.render("I - Insertion | B - Bubble | S - Selction | H - Heap",1,(0,0,0))
    draw_info.window.blit(GUIDE_B,(draw_info.width/2-GUIDE_B.get_width()/2,50+GUIDE.get_height()+10))
    draw_lst(draw_info)
    pygame.display.update()

def generate_lst(n,min_val,max_val):
    lst=[]

    for i in range(n):
        val=random.randint(min_val,max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info,ascending=True):
    lst=draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1=lst[j]
            num2=lst[j+1]
            if((num2 < num1 and ascending) or num2 > num1 and ascending ==False ):
                lst[j],lst[j+1]=num2,num1
                draw_lst(draw_info,j,j+1,True)
                yield True

    return lst 

def selection_sort(draw_info,ascending=True):
    lst=draw_info.lst
    for i in range(len(lst)):
        min_idx = i
        for j in range(i+1, len(lst)):
            if lst[min_idx] > lst[j] and ascending or lst[min_idx]<lst[j] and not ascending:
                min_idx = j        
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_lst(draw_info,i,min_idx,True)
        yield True
    return lst

def Insertion_sort(draw_info,ascending=True):
    lst=draw_info.lst

    for i in range(1, len(lst)):
        key = lst[i]
        # j=i-1
        while True:
            if_ascending=i>0 and lst[i-1]>key and ascending
            if_descending=i>0 and lst[i-1]<key and not ascending
            if not if_ascending and not if_descending:
                break
            lst[i]=lst[i-1]
            i-=1
            lst[i]=key
            draw_lst(draw_info,i,i-1,True)
            yield True
    
    return lst


def heapify(draw_info,lst, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
  

    if l < n and lst[i] < lst[l]:
        largest = l
  
    if r < n and lst[largest] < lst[r]:
        largest = r
  
    # Change root, if needed
    if largest != i:
        lst[i],lst[largest] = lst[largest],lst[i]  # swap
        draw_lst(draw_info,i,0,True)
        # yield True
        heapify(draw_info,lst, n, largest)
  

def heapSort(draw_info,ascending=True):
    lst=draw_info.lst
    n = len(lst)
  
    for i in range(n // 2 - 1, -1, -1):
        heapify(draw_info,lst, n, i)
  
    # One by one extract elements
    for i in range(n-1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]   # swap
        draw_lst(draw_info,i,0,True)
        heapify(draw_info,lst, i, 0)
        yield True

    return lst



def main():
    run=True
    n=50
    min_val=1
    max_val=300
    lst=generate_lst(n,min_val,max_val)
    draw_info=DrawInformation(850,750,lst)
    clock=pygame.time.Clock()
    sorting_algo=bubble_sort
    sorting_algo_name="Bubble Sort"
    ascending=True
    sorting_algo_generator=None
    sorting=False
    while run:
        clock.tick(FPS)
        if sorting:
            try:
                next(sorting_algo_generator)
                draw(draw_info,sorting_algo_name,ascending)
            except StopIteration:
                sorting=False
        else :
            draw(draw_info,sorting_algo_name,ascending)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

            if event.type!=pygame.KEYDOWN:
                continue

            if event.key==pygame.K_r :
                lst=generate_lst(n,min_val,max_val)
                draw_info.set_lst(lst)
                sorting=False   
            elif event.key==pygame.K_SPACE:
                sorting=True
                sorting_algo_generator=sorting_algo(draw_info,ascending)
                print(draw_info.lst)
            elif event.key==pygame.K_a and not sorting:
                ascending=True
            elif event.key==pygame.K_d and not sorting:
                ascending=False
            elif event.key==pygame.K_s and not sorting:
                sorting_algo_name="Selection Sort"
                sorting_algo=selection_sort
            elif event.key==pygame.K_b and not sorting:
                sorting_algo_name="Bubble Sort"
                sorting_algo=bubble_sort
            elif event.key==pygame.K_i and not sorting:
                sorting_algo_name="Insertion Sort"
                sorting_algo=Insertion_sort
            elif event.key==pygame.K_h and not sorting:
                sorting_algo_name="Heap Sort"
                print(draw_info.lst)
                sorting_algo=heapSort
                
    pygame.quit()


if __name__=="__main__":
    main()



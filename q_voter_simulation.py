import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from numba import jit


@jit(nopython=True)
def find_neighbours(agents_net, i, j, N):
    """
    function finding neighbour of drawn voter

    takes
    -----
    agents_net - net with values of voters opinions
    i,j - coordinates of drawn voter in net
    N - size of net

    returns
    -------
    list of existing neighbour

    """
    if i - 1 >= 0:
        left = agents_net[i-1, j]
    else:
        left = 0

    if i + 1 < N:
        right = agents_net[i+1, j]
    else:
        right = 0
        
    if j - 1 >= 0:
        upper = agents_net[i, j-1]
    else:
        upper = 0
        
    if j + 1 < N:
        lower = agents_net[i, j+1]
    else:
        lower = 0

    neighbours = [left, right, upper, lower]
    neighbours = [x for x in neighbours if x != 0]

    return np.array(neighbours)


@jit(nopython=True)
def conformism(choosen, q, agent):
    """
    function setting voter opinion according to conformity

    takes
    -----
    choosen - net of neighbour whose opinion we rely on
    q - group of influence size
    agent - value of opinion of the voter we choosen

    returns
    -------
    new value of opinion of the voter

    """
    opinion = np.sum(choosen)
    
    if opinion == q:
        new_agent = 1
    elif opinion == -q:
        new_agent = -1    
    else:
        new_agent = agent  

    return new_agent


@jit(nopython=True)
def anticonformism(choosen, q, agent):
    """
    function setting voter opinion according to anticonformity

    takes
    -----
    choosen - net of neighbour whose opinion we rely on
    q - group of influence size
    agent - value of opinion of the voter we choosen

    returns
    -------
    new value of opinion of the voter

    """
    opinion = np.sum(choosen)
    
    if opinion == q:
        new_agent = -1
    elif opinion == -q:
        new_agent = 1    
    else:
        new_agent = agent  

    return new_agent


@jit(nopython=True)
def q_model(agents_net, N, q, p, f, anty, repeat): 
    """
    function checking whether change voter opinion

    takes
    -----
    agents_net - net with values of voters opinions
    N - size of net
    q - group of influence size
    p - probability of nonconformity
    f - probability of shift of opinion for independence
    anty - (bool) True for anticonformity and False for independence
    repeat - (bool) whether we draw voters with repeats or not

    returns
    -------
    voters net after one monte carlo step (N^2 changded agents)

    """
    for _ in range(N*N):  
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        agent = agents_net[i, j]

        P = np.random.uniform(0, 1)
        if P > p: # conformity
            neighbours = find_neighbours(agents_net, i, j, N)

            if repeat == True:
                choosen = np.random.choice(neighbours, q, replace=True) 
                agents_net[i, j] = conformism(choosen, q, agent)
            else: 
                if len(neighbours) >= q: # as many neighbour as we want to choose
                    choosen = np.random.choice(neighbours, q, replace=False)
                    agents_net[i, j] = conformism(choosen, q, agent)

        else:  
            if anty == True: # anticonformity
                neighbours = find_neighbours(agents_net, i, j, N)

                if repeat == True:
                    choosen = np.random.choice(neighbours, q, replace=True) 
                    agents_net[i, j] = anticonformism(choosen, q, agent)
                else: 
                    if len(neighbours) >= q:
                        choosen = np.random.choice(neighbours, q, replace=False)
                        agents_net[i, j] = anticonformism(choosen, q, agent)

            else: # independence
                u = np.random.uniform(0, 1)
                if u < f:
                    agents_net[i, j] = -1*agent
    return agents_net

  
def start():
    """
    function after pressing button "START", checks parameters,
    opens new window and shows aimation there

    returns
    -------
    new app window
    
    """
    global stop_anim
    stop_anim = False
    global close_win
    close_win = False 

    window_2 = tk.Toplevel()
    window_2.iconbitmap(default='q_icon.ico')
    window_2.title("Simulation of q-voter model")
    window_2.configure(bg = "white")
    window_2.resizable(False,False) 

    N = eval(N_entry.get())
    q = q_entry.get()
    p = p_entry.get()
    f = f_entry.get()
    r = r_entry.get()

    anty = antykonf.get()
    repeat= replace.get()

    positive = np.ones(int(r*N*N)) # making random net with initial concentration of positive opinion
    negative = -1*np.ones(N*N- len(positive))
    start_vect = np.concatenate((positive, negative), axis=None)
    np.random.shuffle(start_vect)
    agents_net = start_vect.reshape((N, N))

    t = [0]
    data = [np.sum(agents_net)/(N*N)]

    fig = Figure(figsize=(6,6), dpi=100)
    ax = fig.add_gridspec(3, 3)
    ax1 = fig.add_subplot(ax[0:2, 0:2])
    ax2 = fig.add_subplot(ax[2, 0:2])
    fig.set_tight_layout(True)
    ax1.imshow(agents_net, cmap='Purples', interpolation='nearest', vmin=-2, vmax=3)
    ax1.set_title('Czas: {} [MCS]'.format(0))
    ax2.plot(t, data, color='rebeccapurple')
    ax2.set_title('Mean of opinion in time. Now: {:.3f}'.format(data[-1]))
    ax2.set_ylim(-1.1, 1.1)
    
    def animate(i, agents_net, N, q, p, f, anty, repeat):
        """
        function making animation

        takes
        -----
        i - number of animation frame 
        agents_net - net with values of voters opinions
        N - size of net
        q - group of influence size
        p - probability of nonconformity
        f - probability of shift of opinion for independence
        anty - (bool) True for anticonformity and False for independence
        repeat - (bool) whether we draw voters with repeats or not

        returns
        -------
        animation frames

        """
        if not stop_anim:
            agents_net = q_model(agents_net, N, q, p, f, anty, repeat)
            data.append(np.sum(agents_net)/(N*N))
            t.append(t[-1]+1)

            ax1.clear()
            ax1.imshow(agents_net, cmap='Purples', interpolation='nearest', vmin=-2, vmax=2)
            ax1.set_title('Czas: {} [MCS]'.format(t[-1]))

            ax2.clear()
            ax2.plot(t, data, color='rebeccapurple')
            ax2.set_title('Mean of opinion in time. Now: {:.3f}'.format(data[-1]))
            ax2.set_ylim(-1.1, 1.1)
        
        if close_win:
            window_2.destroy()
        
                
    canvas = FigureCanvasTkAgg(fig, window_2)
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)
    anim = FuncAnimation(fig, animate, fargs=(agents_net, N, q, p, f, anty, repeat, ), interval=2, repeat=False)
    canvas.draw() 
    plt.close()


def again():
    """
    function for start button 
    resumes simulation
    """
    global stop_anim
    stop_anim = False


def stop():
    """
    function for pause button 
    pauses simulation
    """
    global stop_anim
    stop_anim = True

def end():
    """
    function for "END" button, 
    closes animation window
    """
    global close_win
    close_win = True


window = tk.Tk()
window.iconbitmap(default='q_icon.ico')
window.title("Q-voter model")
window.configure(bg = "white")

stop_anim = False
close_win = False

font1 = ("Verdana", 15)
font2 = ("Verdana", 10)

tk.Label(window, text="Net size", fg="black", bg="white", font=font2).grid(row=0, column=1, columnspan=2, padx=5, pady=5)
N_entry = tk.Entry(window, font=font2, bg="white", width=20)
N_entry.grid(row=1, column=1, columnspan=2, pady=7)

tk.Label(window, text="Group of influence size", fg="black", bg="white", font=font2).grid(row=2, column=1, columnspan=2, padx=5, pady=5)
q_entry = tk.Scale(window, from_=1, to=4, font=font2, bg="white", bd=0, length=200, orient=tk.HORIZONTAL)
q_entry.grid(row=3, column=1, columnspan=2, pady=7)

tk.Label(window, text="Initial concentration of positive opinion", fg="black", bg="white", font=font2).grid(row=4, column=1, columnspan=2, padx=5, pady=5)
r_entry = tk.Scale(window, from_=0, to=1, resolution=0.01, font=font2, bg="white", bd=0, length=200, orient=tk.HORIZONTAL)
r_entry.grid(row=5, column=1, columnspan=2, pady=7)

tk.Label(window, text="Probability of nonconformity", fg="black", bg="white", font=font2).grid(row=6, column=1, columnspan=2, padx=5, pady=5)
p_entry = tk.Scale(window, from_=0, to=1, resolution=0.01, font=font2, bg="white", bd=0, length=200, orient=tk.HORIZONTAL)
p_entry.grid(row=7, column=1, columnspan=2, pady=7)

tk.Label(window, text="Probability of shift of opinion in independence", fg="black", bg="white", font=font2).grid(row=8, column=1, columnspan=2, padx=5, pady=5)
f_entry = tk.Scale(window, from_=0, to=1, resolution=0.01, font=font2, bg="white", bd=0, length=200, orient=tk.HORIZONTAL)
f_entry.grid(row=9, column=1, columnspan=2, pady=7)

tk.Label(window, text="Model type", fg="black", bg="white", font=font2).grid(row=10, column=0, columnspan=4, padx=5, pady=5)
antykonf = tk.IntVar()
antykonf.set(0)
indep = tk.Radiobutton(window, text="Independence", font=font2, bg="white", variable=antykonf, value=0)
indep.grid(row=11, column=0, columnspan=2, padx=5, pady=7)
anty_konf = tk.Radiobutton(window, text="Anticonformity", font=font2, bg="white", variable=antykonf, value=1)
anty_konf.grid(row=11, column=2, columnspan=2, padx=5, pady=7)

tk.Label(window, text="Drawing neighbour", fg="black", bg="white", font=font2).grid(row=12, column=0, columnspan=4, padx=5, pady=5)
replace = tk.IntVar()
replace.set(1)
rep = tk.Radiobutton(window, text="With repeats", font=font2, bg="white", variable=replace, value=1)
rep.grid(row=13, column=0, columnspan=2, padx=5, pady=7)
non_rep = tk.Radiobutton(window, text="Without repeats", font=font2, bg="white", variable=replace, value=0)
non_rep.grid(row=13, column=2, columnspan=2, padx=5, pady=7)

button_start = tk.Button(window, text="START", font=font1, fg="white", bg="#cc0000", command=start)
button_start.grid(row=14, column=1, padx=2, pady=5)

button_end = tk.Button(window, text="END", font=font1, fg="white", bg="#cc0000", command=end)
button_end.grid(row=14, column=2, padx=2, pady=5)

button_again = tk.Button(window, text="\u23F5", font=font1, fg="white", bg="#cc0000", command=again) 
button_again.grid(row=14, column=1, padx=2, pady=5, sticky=tk.E)

button_stop = tk.Button(window, text="\u23F8", font=font1, fg="white", bg="#cc0000", command=stop) 
button_stop.grid(row=14, column=2, padx=2, pady=5, sticky=tk.W)
 
window.mainloop()
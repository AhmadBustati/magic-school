# magic-school
This project aims to ease  the communication between a student's parent, and the school board  

## Mobile 
It has two mobile : one for the teacher, and the other for  the parents. Developed using Java by [Mahmoud Allouh](https://github.com/kanfoush) 
### The teacher can  : 
*  Enter a mark for student for an exam or a quiz. 
*  Send a PDF file containg a homework via the app. 
*  Contact the parent for a specific problem.
*  Send a student's activity relative to the student's behavior that day. 
*  View a calander showing his/her lessons.
*  Genrate a question using a neural network explained furhter [here](##Neural-Networks)
### The parent can : 
* View notifications sent by the school either specific to the child(scored poorly on a quiz), or genral(there will be next sunday)
* Send homework requested by a teacher 
* View student's degrees on all subjects, and their percentage 
* View student's attendnce record (when he missed school and whether that was explained by the parent)  
* Send either a feedback or a complaint to the headmaster 
* Contact a teacher 
* View a calander where the daily lessons apper 
* View the activty of the student 

## Dashboard for the school administration 
Same interface with different access to either the headmaster or an employee with administrative access. Developed with JavaScript by []()
### The employee can :
* 




## Neural Networks 
There are two neural networks used in this project :
### 1.FaceNet for face recognition : 
Developed by google in 2015 [paper](https://arxiv.org/abs/1503.03832)

### 2. A fine tuned T5 network for question generation :
Dataset used for fine tuning from [ugging face](https://huggingface.co/datasets/iarfmoose/question_generator)
the original paper for the [t5](https://arxiv.org/abs/1910.10683) which was also developed by google but in 2020

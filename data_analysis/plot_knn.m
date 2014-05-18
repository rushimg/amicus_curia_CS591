x = [2 5 10 20 30];

baseline = [0.8507 0.8507 0.8507 0.8507 0.8507];
reps = [0.83539 0.8416 0.8532 0.8461 0.8461];
orgs =[0.8339 0.8339 0.83971 0.85269 0.85204];

plot(x,baseline,'m-o');
hold on;
plot(x,reps,'b-o');
hold on;
plot(x,orgs,'g-o');



title('Classification Accuracy vs. k')
xlabel('k')
ylabel('Accuracy')
legend('Baseline','kNN Representatives','kNN Intrest Groups')
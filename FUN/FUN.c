#include <stdio.h>
#include <windows.h> // Required for Sleep()

int main() {
    printf("Think a number(between 1-10000).\n");
    Sleep(200);
    
    printf("Multiply it by 2.\n");
    Sleep(300);
    
    printf("Add 50 in the product.\n");
    Sleep(400);
    
    printf("Now divide the answer of your number by 2.\n");
    Sleep(400);
    
    printf("Last, minus the number you think in the answer.\n");
    Sleep(400);
    
    printf("Answer is 25?(y/n): ");
    
    char a;
    scanf(" %c", &a); // Space before %c to ignore newline
    Sleep(900);
    if(a == 'y'){
        printf("Yes, We got it!\n");
    }
    else if (a == 'n'){
        printf("Let's retry, I hope there was a mistake in the calculation!\n");
        Sleep(400);

        int b;
        printf("Enter the number you thought of: ");
        scanf("%d", &b);
        if (b>10000){            printf("Incorrect number, thecode can handle a number upto 2147483647 while  thought that 10000 is enough, this tric work with all number but due to a limit, it is not be possible to use this trick upto 10000, if want , remove if statament from here.\n");
            return(0);
        }
        int step1 = b * 2;
        printf("Step 1: %d x 2 = %d\n", b, step1);
        Sleep(400);

        int step2 = step1 + 50;
        printf("Step 2: %d + 50 = %d\n", step1, step2);
        Sleep(300);

        int step3 = step2 / 2;
        printf("Step 3: %d / 2 = %d\n", step2, step3);
        Sleep(200);
        int result = step3 - b;
        printf("Step 4: %d - %d = %d\n", step3, b, result);
        Sleep(300);
        if(result == 25){
            printf("Your calculation had a mistake!\n");
        } else {
            printf("Oops! This trick didn't work with your number %d\n", b);
        }
    }

    return 0;
}

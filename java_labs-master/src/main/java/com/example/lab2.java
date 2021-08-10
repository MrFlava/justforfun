package lab2;





import lab2.matrix.Matrix;

import lab2.matrix.MatrixCalculator;

import lab2.matrix.MatrixManager;




import java.util.Scanner;



public class Main {




    public static void main(String[] args) throws Exception {

        System.out.println(Lab1Constants.WELCOME_MESSAGE);

        Scanner scanner = new Scanner(System.in);




        // Read width

        System.out.println("Enter matrix height below:");

        int matrix_height = Integer.parseInt(scanner.nextLine());




        // Read height

        System.out.println("Enter matrix width below:");

        int matrix_width = Integer.parseInt(scanner.nextLine());




        // Read is_random var, it means should we create matrix in random way

        System.out.println("Write 'y' if you want to fill matrix in random way.");

        boolean is_random = "y".equals(scanner.nextLine());




        // matrix creation

        MatrixManager matrixManager = new MatrixManager();

        Matrix matrix = matrixManager.create_matrix(is_random, matrix_width, matrix_height);




        matrixManager.validateMatrixParameters(matrix);

        matrixManager.showMatrix(matrix);






        // process calculations

        MatrixCalculator matrixCalculator = new MatrixCalculator();




        double average = matrixCalculator.calculateMatrixAverage(matrix);

        int minimumElement = matrixCalculator.getMatrixMinimumElement(matrix);

        int maximumElement = matrixCalculator.getMatrixMaximumElement(matrix);







        System.out.printf("\nAverage value: %f\n", average);

        System.out.printf("Minimum value: %d\n", minimumElement);

        System.out.printf("Maximum value: %d\n", maximumElement);

    }

}

package lab2;



public interface Lab1Constants {

    int UPPER_RANDOM_RANGE = 100;

    int LOWER_RANDOM_RANGE = 1;
}

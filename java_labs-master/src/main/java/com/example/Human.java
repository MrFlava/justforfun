package lab3;





import lab3.controllers.UniversityCreatorManually;

import lab3.controllers.UniversityRandomCreator;

import lab3.models.universityUnits.University;




import java.util.Scanner;




public class Main {

    public static void main(String[] args) throws Exception {

        University university = createUniversity();

        System.out.println(university);

    }




    public static University createUniversity() throws Exception {

        University university;

        Scanner scanner = new Scanner(System.in);




        System.out.print(Constants.ANSI_PURPLE + "Do you want to create university manually? (y/n): ");

        boolean isManually = "y".equals(scanner.nextLine());




        if (isManually) {

            university = new UniversityCreatorManually().run();

        } else {

            university = new UniversityRandomCreator().run();

        }

        return university;

    }

}


package lab3;





import lab3.models.Sex;




import java.util.List;




public class Utils {




    public static String listToString(List<?> list, int indent) {

        String tab_indent = resolveIndent(indent);




        StringBuilder result = new StringBuilder("");

        for (Object o : list) {

            result.append("\n").append(tab_indent).append(o);

        }

        return result.toString();

    }




    private static String resolveIndent(int indent) {

        StringBuilder result = new StringBuilder();

        for (int i = 0; i < indent; i++) {

            result.append("\t");

        }

        return result.toString();

    }




    public static Sex defineSex(String input) {

        Sex sex;




        switch(input) {

            case "male":

            case "m":

                sex = Sex.MALE;

                break;

            case "female":

            case "f":

                sex = Sex.FEMALE;

                break;

            default:

                throw new IllegalStateException("Unexpected value: " + input);

        }

        return sex;

    }

}



package lab4;





import com.google.gson.Gson;

import lab3.models.universityUnits.University;



import java.io.*;




public class JsonManager {




    public void writeObjectToJson(Object o, String filePath) {

        Gson gson = new Gson();




        String json = gson.toJson(o);

        try {

            FileWriter myWriter = new FileWriter(filePath);

            myWriter.write(json);

            myWriter.close();

            System.out.println("Successfully wrote to the file.");

        } catch (IOException e) {

            System.out.println("An error occurred.");

            e.printStackTrace();

        }

    }


    public Object readObjectFromJson(String filePath) {

        Gson gson = new Gson();

        try {

            return gson.fromJson(new FileReader(filePath), University.class);

        } catch (FileNotFoundException e) {

            e.printStackTrace();

        }

        return null;

    }

}


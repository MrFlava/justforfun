package lab5;





import lab5.game.BlackJackController;




public class Main {

    public static void main(String[] args) {

       new BlackJackController().play();

    }

}




package lab5;





import java.util.List;

import java.util.stream.Collectors;




public class Utils {

    public int resolvePoints(List<String> cards) {

        List<String> result = cards.stream().map(n -> n.substring(0, n.length() - 1))

                                    .collect(Collectors.toList());




        int points = 0;

        for (String card : result) {

            points += convertComplexCards(card);

        }

        return points;

    }




    private int convertComplexCards(String card) {

        int points;

        switch (card){

            case "j":

            case "q":

            case "k":

                points = 10;

                break;

            case "a":

                points = 2;

                break;

            default:

                points = Integer.parseInt(card);

        }

        return points;

    }

}

package lab5.game;






import java.util.Arrays;

import java.util.List;

import java.util.Random;

import java.util.stream.Collectors;







public class BlackJack {

    private List<String> cards;




    public BlackJack() {

        this.cards = getCardsSet();

    }




    public List<String> getCards() {

        return this.cards;

    }




    public void setCards(List<String> cards) {

        this.cards = cards;

    }




    private List<String> getCardsSet() {

        return Arrays.asList(

                "2D", "2H", "2S", "2C",

                "3D", "3H", "3S", "3C",

                "4D", "4H", "4S", "4C",

                "5D", "5H", "5S", "5C",

                "6D", "6H", "6S", "6C",

                "7D", "7H", "7S", "7C",

                "8D", "8H", "8S", "8C",

                "9D", "9H", "9S", "9C",

                "10D", "10H", "10S", "10C",

                "jD", "jH", "jS", "jC",

                "qD", "qH", "qS", "qC",

                "kD", "kH", "kS", "kC",

                "aD", "aH", "aS", "aC"

        );

    }

}
package lab5.game;






import lab5.Utils;

import lab5.players.models.PCPlayer;

import lab5.players.models.UserPlayer;




import java.util.List;

import java.util.Random;

import java.util.Scanner;

import java.util.stream.Collectors;




public class BlackJackController {

    public void play() {

        BlackJack blackJack = new BlackJack();

        Utils utils = new Utils();

        Scanner scanner = new Scanner(System.in);




        PCPlayer pcPlayer = new PCPlayer();

        pcPlayer.initCards();




        UserPlayer userPlayer = new UserPlayer();

        userPlayer.initCards();




        boolean isPCPlayerContinuePlaying = true;

        boolean isUserPlayerContinuePlaying = true;




        while (isPCPlayerContinuePlaying) {

            pcPlayer.takeCard(getCard(blackJack));

            pcPlayer.setPoints(utils.resolvePoints(pcPlayer.getCards()));




            if (pcPlayer.getPoints() > PCPlayer.POINTS_THRESHOLD) {

                isPCPlayerContinuePlaying = false;

            }

        }




        userPlayer.takeCard(getCard(blackJack));




        while(isUserPlayerContinuePlaying) {

            userPlayer.takeCard(getCard(blackJack));

            System.out.print("Now you have: ");

            System.out.println(userPlayer.getCards() + " cards.");




            System.out.print("Do you want to take more? (y/n) ");

            isUserPlayerContinuePlaying = "y".equals(scanner.nextLine());

        }

        int pcPlayerPoints = pcPlayer.getPoints();




        userPlayer.setPoints(utils.resolvePoints(userPlayer.getCards()));

        int userPlayerPoints = userPlayer.getPoints();







        if ((pcPlayerPoints <= 21 && pcPlayerPoints > userPlayerPoints) || (userPlayerPoints > 21 && pcPlayerPoints < 21)) {

            System.out.println("\nPC Player win\n");

        } else if ((userPlayerPoints <=21 && userPlayerPoints > pcPlayerPoints) || (pcPlayerPoints > 21 && userPlayerPoints < 21)) {

            System.out.println("\nUser player win\n");

        } else {

            System.out.println("\nDraw\n");

        }




        System.out.println("PC Player cards: " + pcPlayer.getCards() + ", points: " + pcPlayerPoints);

        System.out.println("User Player cards: " + userPlayer.getCards() + ", points: " + userPlayerPoints);

    }




    public String getCard(BlackJack blackJack) {

        Random random = new Random();

        List<String> cards = blackJack.getCards();




        String randomCard = cards.get(random.nextInt(cards.size()));

        blackJack.setCards(removeCardFromSet(cards, randomCard));

        return randomCard;

    }




    private List<String> removeCardFromSet(List<String> cards, String randomCard) {

        return cards.stream().filter(n -> (!n.equals(randomCard)))

                .collect(Collectors.toList());

    }

}
package lab5.players.models;





import java.util.ArrayList;

import java.util.List;




abstract public class BasePlayer {

    private List<String> cards;

    private int points;




    abstract public void takeCard(String newCard);




    public void initCards() {

        this.cards = new ArrayList<String>();

    }




    public void addCard(String card) {

        this.cards.add(card);

    }




    public List<String> getCards() {

        return this.cards;

    }




    public void setPoints(int points) {

        this.points = points;

    }




    public int getPoints() {

        return this.points;

    }

}

package lab5.players.models;





public class PCPlayer extends BasePlayer {

    public static final int POINTS_THRESHOLD = 17;




    @Override

    public void takeCard(String newCard) {

        this.addCard(newCard);

    }

}

package lab5.players.models;





public class UserPlayer extends BasePlayer {

    @Override

    public void takeCard(String newCard) {

        this.addCard(newCard);

    }

}

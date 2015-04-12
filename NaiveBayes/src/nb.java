import java.io.*;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Scanner;
import java.util.regex.Pattern;

/**
 * Created by amaliujia on 15-4-4.
 */
public class nb {
    //ArrayList<Integer> frqOfToken;
    //ArrayList<Integer> frqOfToken;
    HashMap<String, Integer> frqMap1;
    HashMap<String, Integer> frqMap2;
    HashMap<String, Integer> valu;
    int totalVal = 0;
    int terms1 = 0;
    int terms2 = 0;
    int tokens1 = 0;
    int tokens2 = 0;
    int docs = 0;
    int docs1 = 0;
    int docs2 = 0;

    HashMap<String, Double> pMap1;
    HashMap<String, Double> pMap2;
    double p1 = 0.0;
    double p2 = 0.0;


    public nb(){
        frqMap1 = new HashMap<String, Integer>();
        frqMap2 = new HashMap<String, Integer>();
        pMap1 = new HashMap<String, Double>();
        pMap2 = new HashMap<String, Double>();
        valu = new HashMap<String, Integer>();
    }


    public static void main(String[]args){
        String Train = args[0];
        String Test = args[1];

        nb naive = new nb();
        try {
            naive.train(Train);
            naive.test(Test);
        } catch (IOException e) {
            e.printStackTrace();
        }

        // System.out.print("1");
    }

    private void test(String testPath) throws IOException {
        int hit = 0;
        int total = 0;

        BufferedReader scanner = null;
        try {
            scanner = new BufferedReader(new FileReader(new File(testPath))); //new Scanner(new File(testPath));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        String path = null;
        while ((path = scanner.readLine()) != null){
            total += 1;
            //String path = scanner.nextLine();
            int result = 0;
            try {
                result = bayse(path);
            } catch (IOException e) {
                e.printStackTrace();
            }

            if(Pattern.matches("con.*", path) && result == 1){
                hit++;
            }else if(Pattern.matches("lib.*", path) && result == 0) {
                hit++;
            }
        }
        System.out.printf("Accuracy: %.04f", (hit * 1.0)  / (total * 1.0));

    }

    private int bayse(String instance) throws IOException {
        double pp1 = 0.0;
        double pp2 = 0.0;
        //Scanner scanner = null;
        BufferedReader scanner = null;
        try {
            scanner = new BufferedReader(new FileReader(new File(instance))); //new Scanner(new File(instance));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        String line = "";
        //Scanner scanner1 = new Scanner(p);
        while ((line = scanner.readLine()) != null){
            //line = scanner.nextLine().toLowerCase(Locale.ENGLISH);
            line = line.toLowerCase();
            if(pMap1.containsKey(line)){
                pp1 += pMap1.get(line);// Math.log(pMap1.get(line));
            }else{
                // pp1 += Math.log(((1.0) / (tokens1 * 1.0 + (totalVal) * 1.0)));
            }

            if(pMap2.containsKey(line)){
                pp2 += pMap2.get(line); //Math.log(pMap2.get(line));
            }else {
                // pp2 += Math.log((1.0) / (tokens2 * 1.0 + (totalVal) * 1.0));
            }

        }
        pp1 += p1;//Math.log(p1);
        pp2 += p2;//Math.log(p2);

        if(pp1 > pp2){
            System.out.println("C");
            return 1;
        }else{
            System.out.println("L");
            return 0;
        }

    }

    private void train(String trainPath) throws IOException {
        Scanner scanner = null;
        try {
            scanner = new Scanner(new File(trainPath));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        while (scanner.hasNext()){
            docs++;
            String p = scanner.nextLine();
            //Scanner subScanner = null;
            BufferedReader subScanner = null;
            try {
                subScanner = new BufferedReader(new FileReader(new File(p))); //new Scanner(new File(p));
            } catch (IOException e) {
                e.printStackTrace();
            }
            if(Pattern.matches("con.*", p)){
                docs1++;
                String line = null;
                while ((line = subScanner.readLine()) != null){
                    tokens1++;
                    line = line.toLowerCase();
                    //line = subScanner.nextLine().toLowerCase(Locale.ENGLISH);
                    if(!frqMap1.containsKey(line)){
                        terms1++;
                        frqMap1.put(line, 1);
                    }else{
                        frqMap1.put(line, frqMap1.get(line) + 1);
                    }

                    if(!valu.containsKey(line)){
                        valu.put(line, 1);
                        totalVal += 1;
                    }
                }
            }else{
                docs2++;
                String line = "";
                while ((line = subScanner.readLine()) != null){
                    tokens2++;
                    line = line.toLowerCase();
                    //line = subScanner.nextLine().toLowerCase(Locale.ENGLISH);
                    if(!frqMap2.containsKey(line)){
                        terms2++;
                        frqMap2.put(line, 1);
                    }else{
                        frqMap2.put(line, frqMap2.get(line) + 1);
                    }

                    if(!valu.containsKey(line)){
                        valu.put(line, 1);
                        totalVal += 1;
                    }
                }
            }
        }

        double val = totalVal; //frqMap1.size() + frqMap2.size();

        Iterator iterator = valu.keySet().iterator();
        while (iterator.hasNext()){
            String s = (String) iterator.next();
            if(frqMap1.containsKey(s)){
                int n = frqMap1.get(s);
                double p = Math.log((n * 1.0 + 1.0) / (tokens1 * 1.0 + val));
                pMap1.put(s, p);
            }else{
                int n = 0;
                double p =  Math.log((n * 1.0 + 1.0) / (tokens1 * 1.0 + val));
                pMap1.put(s, p);
            }

            if(frqMap2.containsKey(s)){
                int n = frqMap2.get(s);
                double p =  Math.log((n * 1.0 + 1.0) / (tokens2 * 1.0 + val));
                pMap2.put(s, p);
            }else{
                int n = 0;
                double p =  Math.log((n * 1.0 + 1.0) / (tokens2 * 1.0 + val));
                pMap2.put(s, p);
            }
        }

        p1 =  Math.log(docs1 * 1.0 / docs * 1.0);
        p2 =  Math.log(docs2 * 1.0 / docs * 1.0);

    }

}

import java.io.*;
import java.util.*;
import java.util.regex.Pattern;

/**
 * Created by amaliujia on 15-4-6.
 */
public class topwordsLogOdds {
    //ArrayList<Integer> frqOfToken;
    HashMap<String, Integer> frqMap1;
    HashMap<String, Integer> frqMap2;
    HashMap<String, Integer> valu;
    int totalVal = 0;
    int terms1;
    int terms2;
    int tokens1;
    int tokens2;
    int docs;
    int docs1;
    int docs2;

    HashMap<String, Double> pMap1;
    HashMap<String, Double> pMap2;
    HashMap<String, Double> ppMap;
    HashMap<String, Double> ppMap2;
    double p1;
    double p2;

    int hit;
    int total;


    public topwordsLogOdds(){
        frqMap1 = new HashMap<String, Integer>();
        frqMap2 = new HashMap<String, Integer>();
        pMap1 = new HashMap<String, Double>();
        pMap2 = new HashMap<String, Double>();
        valu = new HashMap<String, Integer>();
        ppMap = new HashMap<String, Double>();
        ppMap2 = new HashMap<String, Double>();
    }


    public static void main(String[]args){
        String Train = args[0];
        //String Test = args[1];

        //Naive naive = new Naive();
        topwordsLogOdds naive = new topwordsLogOdds();
        try {
            naive.train(Train);
        } catch (IOException e) {
            e.printStackTrace();
        }
        //naive.test(Test);

        List<Map.Entry<String, Double>> folder = new ArrayList<Map.Entry<String, Double>>(naive.ppMap2.entrySet());
        Collections.sort(folder, new Comparator<Map.Entry<String, Double>>() {
            public int compare(Map.Entry<String, Double> e1,
                               Map.Entry<String, Double> e2) {
                if (!e1.getValue().equals(e2.getValue())) {
                    if (e2.getValue() > e1.getValue()) return 1;
                    else return -1;
                } else
                    return (e1.getKey()).toString().compareTo(e2.getKey().toString());
            }
        });

        for(int i = 0; i < 20; i++){
            System.out.printf(folder.get(i).getKey() + " %.04f" + "\n", folder.get(i).getValue());

        }

        System.out.printf("\n");


        folder = new ArrayList<Map.Entry<String, Double>>(naive.ppMap.entrySet());
        Collections.sort(folder, new Comparator<Map.Entry<String, Double>>() {
            public int compare(Map.Entry<String, Double> e1,
                               Map.Entry<String, Double> e2) {
                if (!e1.getValue().equals(e2.getValue())) {
                    if (e2.getValue() > e1.getValue()) return 1;
                    else return -1;
                } else
                    return (e1.getKey()).toString().compareTo(e2.getKey().toString());
            }
        });

        for(int i = 0; i < 20; i++){
            System.out.printf(folder.get(i).getKey() + " %.04f" + "\n", folder.get(i).getValue());

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
        while (iterator.hasNext()) {
            String s = (String) iterator.next();
            if (frqMap1.containsKey(s)) {
                int n = frqMap1.get(s);
                double p = (n * 1.0 + 1.0) / (tokens1 * 1.0 + val);
                pMap1.put(s, p);
            } else {
                int n = 0;
                double p = (n * 1.0 + 1.0) / (tokens1 * 1.0 + val);
                pMap1.put(s, p);
            }

            if (frqMap2.containsKey(s)) {
                int n = frqMap2.get(s);
                double p = (n * 1.0 + 1.0) / (tokens2 * 1.0 + val);
                pMap2.put(s, p);
            } else {
                int n = 0;
                double p = (n * 1.0 + 1.0) / (tokens2 * 1.0 + val);
                pMap2.put(s, p);
            }

            //compute
            ppMap.put(s, Math.log(pMap1.get(s) / pMap2.get(s)));
            ppMap2.put(s, Math.log(pMap2.get(s) / pMap1.get(s)));
        }

    }
}

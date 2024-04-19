import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

// A class representing mathematical vectors and operations on them
class Vector {
    private final double[] values; // Array to hold vector values

    // Constructor to initialize a vector of given size with zeros
    public Vector(int size) {
        this.values = new double[size];
    }

    // Constructor to initialize a vector with given values
    public Vector(double ... values) {
        this.values = Arrays.copyOf(values, values.length);
    }

    // Method to get the size of the vector
    public int size() {
        return values.length;
    }

    // Method to get the value at a specific index in the vector
    public double value(int n) {
        return values[n];
    }

    // Method to calculate the length (magnitude) of the vector
    public double length() {
        double sum = Arrays.stream(values)
                .map(v -> v * v)
                .sum();
        return Math.sqrt(sum);
    }

    // Method to calculate the negative of the vector
    public Vector negative() {
        double[] newValues = Arrays.stream(values)
                .map(v -> -v)
                .toArray();
        return new Vector(newValues);
    }

    // Method to calculate the normalized version of the vector
    public Vector normalized() {
        double length = length();
        double[] newValues = Arrays.stream(values)
                .map(v -> v / length)
                .toArray();
        return new Vector(newValues);
    }

    // Method to add another vector to this vector
    public Vector add(Vector v) {
        ensureMatchingSizes(v);

        double[] newValues = new double[size()];
        for (int i = 0; i < size(); ++i)
            newValues[i] = value(i) + v.value(i);

        return new Vector(newValues);
    }

    // Method to subtract another vector from this vector
    public Vector subtract(Vector v) {
        ensureMatchingSizes(v);

        double[] newValues = new double[size()];
        for (int i = 0; i < size(); ++i)
            newValues[i] = value(i) - v.value(i);

        return new Vector(newValues);
    }

    // Method to multiply the vector by a scalar
    public Vector multiply(double multiplier) {
        double[] newValues = Arrays.stream(values)
                .map(v -> v * multiplier)
                .toArray();
        return new Vector(newValues);
    }

    // Method to calculate the Euclidean distance between this vector and another vector
    public double distance(Vector v) {
        ensureMatchingSizes(v);

        double sum = 0;
        for (int i = 0; i < size(); ++i)
            sum += Math.pow(value(i) - v.value(i), 2);

        return Math.sqrt(sum);
    }

    // Method to calculate the dot product of this vector and another vector
    public double dotProduct(Vector v) {
        ensureMatchingSizes(v);

        double sum = 0;
        for (int i = 0; i < size(); ++i)
            sum += value(i) * v.value(i);

        return sum;
    }

    // Private method to ensure that vectors have matching sizes for operations
    private void ensureMatchingSizes(Vector v) {
        if (this.size() != v.size())
            throw new NotMatchingSizesException("sizes: " + size() + " and " + v.size());
    }

    // Method to convert the vector to a string representation
    @Override
    public String toString() {
        return Arrays.toString(values);
    }

    // Exception class to handle cases where vector sizes do not match for operations
    private static class NotMatchingSizesException extends RuntimeException {
        public NotMatchingSizesException() {
        }

        public NotMatchingSizesException(String message) {
            super(message);
        }

        public NotMatchingSizesException(String message, Throwable cause) {
            super(message, cause);
        }

        public NotMatchingSizesException(Throwable cause) {
            super(cause);
        }

        public NotMatchingSizesException(String message, Throwable cause, boolean enableSuppression,
                                         boolean writableStackTrace)
        {
            super(message, cause, enableSuppression, writableStackTrace);
        }
    }
}

//------------------------------------------------------------------------------------------------------------------------

// A class to load language data from files into a list of observations
class DataLoader {

    // Method to load language data from a directory and return a list of observations
    static List<Observation> loadLanguageData(String trainDirectory) {
        try {
            return Files.walk(Path.of(trainDirectory), 1)
                    .skip(1)
                    .filter(Files::isDirectory)
                    .map(DataLoader::loadWordFiles)
                    .flatMap(Collection::stream)
                    .collect(Collectors.toList());
        }
        catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    // Private method to load word files and convert them into observations
    private static List<Observation> loadWordFiles(Path path) {
        String language = path.getFileName().toString();

        try {
            return Files.walk(path, 1)
                    .filter(Files::isRegularFile)
                    .map(DataLoader::loadStatisticVector)
                    .map(vector -> new Observation(vector, language))
                    .collect(Collectors.toList());
        }
        catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    // Private method to load statistic vectors from files
    private static Vector loadStatisticVector(Path path) {
        try {
            String fileContents = Files.readString(path);

            return getStatisticsVector(fileContents);
        }
        catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    // Method to calculate statistic vector from text data
    public static Vector getStatisticsVector(String text) {
        double[] counts = new double['z' - 'a' + 1];

        for (char c : text.toLowerCase().toCharArray()) {
            if (c >= 'a' && c <= 'z')
                ++counts[c - 'a'];
        }

        Vector v = new Vector(counts);
        return v.normalized();
    }
}

//---------------------------------------------------------------------------------------------------------

// A class representing an observation, containing a vector and its classification
class Observation {
    private Vector vector;
    private String classification;

    public Observation(Vector vector, String classification) {
        this.vector = vector;
        this.classification = classification;
    }

    public Vector getVector() {
        return vector;
    }

    public String getClassification() {
        return classification;
    }

    @Override
    public String toString() {
        return classification + ": " + vector.toString();
    }
}

//-----------------------------------------------------------------------------------------------------------

// A subclass of Observation for binary classification
class BinaryObservation extends Observation {
    private int value;

    public BinaryObservation(Vector vector, String classification, int value) {
        super(vector, classification);
        this.value = value;
    }

    public BinaryObservation(Observation observation, int value) {
        super(observation.getVector(), observation.getClassification());
        this.value = value;
    }

    public int getClassificationValue() {
        return value;
    }
}

//-------------------------------------------------------------------------------------------------------------

// A class representing a neural network
class Network {
    private final double MAX_ERROR = 0.01;
    private final int MAX_ITERATIONS = 50_000;

    private final Map<String, Integer> observationIds;
    private final Perceptron[] perceptrons;

    // Initializes the network with input parameters such as the size of the input vectors,
    // the number of classifications, and a map of observation IDs.
    public Network(int inputSize, int classificationCount, double alpha, Map<String, Integer> observationIds) {
        this.observationIds = observationIds;
        perceptrons = new Perceptron[classificationCount];
        for (int i = 0; i < classificationCount; ++i)
            perceptrons[i] = new Perceptron(alpha, alpha, inputSize);
    }

    //Classifies an observation by computing the outputs of all perceptrons
    // and selecting the classification with the highest output.
    //Returns the classification label along with the confidence scores for each classification.
    public String classify(Observation observation) {
        double[] result = new double[perceptrons.length];
        for (int i = 0; i < perceptrons.length; i++)
            result[i] = perceptrons[i].classify(observation.getVector());

        int maxId = maxId(result);

        String classification = observationIds.entrySet().stream().filter(e -> e.getValue() == maxId).findFirst().get().getKey();

        return classification + " " + Arrays.stream(result).boxed().map(str -> String.format("%.2f", str)).collect(Collectors.joining(", ", "[", "]"));
    }

    // Method to find the index of the maximum value in an array
    private int maxId(double[] arr) {
        int maxId = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[maxId] < arr[i])
                maxId = i;
        }
        return maxId;
    }

    //Trains the network using a list of observations.
    //It iterates over the training data until either the maximum number of
    // iterations is reached or the error falls below the maximum acceptable error.
    //Prints the error value achieved during training and the number of iterations performed.
    public void train(List<Observation> observations) {
        double error = 1;

        int i = 0;
        for (; i < MAX_ITERATIONS && error > MAX_ERROR; i++)
            error = performIteration(observations);

        System.out.println("Error value achieved during the training process: "+ error);
        System.out.println("Number of iterations performed during the training process: "+ i);
        System.out.println("--------------------------------------------------");
    }

    //Performs one training iteration by iterating over all observations in the training data
    // and updating the perceptrons accordingly.
    //Computes the average error over all observations in the iteration.
    private double performIteration(List<Observation> observations) {
        double sum = 0;

        for (Observation observation : observations)
            sum += trainObservation(observation);

        double error = sum / observations.size();
        return error;
    }

    //Trains a single observation by updating the perceptrons based on the observation's classification.
    //It calculates the error for each perceptron and returns the average error.
    private double trainObservation(Observation observation) {
        double sum = 0;

        for (int i = 0; i < perceptrons.length; ++i) {
            BinaryObservation bObservation = new BinaryObservation(
                    observation,
                    observationIds.get(observation.getClassification()) == i ? 1 : 0
            );
            sum += perceptrons[i].trainObservation(bObservation);
        }

        double error = sum / perceptrons.length;
        return error;
    }
}

//------------------------------------------------------------------------------------------

// A class representing a single perceptron
class Perceptron {
    private double alpha;
    private double beta;

    private Vector weights;
    private double theta = 0;
    //activation function of the perceptron.
    private final Function<Double, Double> thresholdFunction = net -> 1 / (1 + Math.exp(-net));

    // Constructor to initialize a perceptron with given parameters
    public Perceptron(double alpha, double beta, int inputCount) {
        this.alpha = alpha;
        this.beta = beta;
        this.weights = getRandomWeights(inputCount);
    }

    // Method to generate random weights for the perceptron
    private static Vector getRandomWeights(int size) {
        Random random = new Random();
        double[] values = random.doubles(size).toArray();
        return new Vector(values);
    }

    //Classifies an input vector by computing the dot product of the input vector
    // and the weights, applying the activation function, and returning the result.
    public double classify(Vector inputVector) {
        double net = weights.dotProduct(inputVector) - theta;
        return thresholdFunction.apply(net);
    }

    //Trains the perceptron with a binary observation (a labeled input vector).
//Adjusts the weights and threshold based on the observed classification value and the predicted output.
//Computes the error and returns it.
    public double trainObservation(BinaryObservation observation) {
        //input vector
        Vector x = observation.getVector();
        //true classification value
        int d = observation.getClassificationValue();
        //predicted output
        double y = classify(x);
        //difference between the true classification value (d) and the predicted output (y).
        // The error signal is multiplied by the derivative of the activation function
        // to adjust the weights and bias of the perceptron during training.

        //error signal in a sigmoid activation function.
        double errorSignal = (d - y) * y * (1 - y);

        weights = weights.add(x.multiply(alpha * errorSignal));
        //update threshold
        theta = theta - beta * errorSignal;

        double error =  Math.pow(d - y, 2);
        return error;
    }
}

//------------------------------------------------------------------------------------------------

// Main class to run the program
public class Main {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);

        final String trainDirectory = "data/train";
        final String testDirectory = "data/test";

        // Load training data
        List<Observation> trainObservations = DataLoader.loadLanguageData(trainDirectory);
        Map<String, Integer> classMap = mapObservationsToIds(trainObservations);

        int inputSize = 'z' - 'a' + 1;
        Network network = new Network(inputSize, classMap.size(), 0.005, classMap);
        network.train(trainObservations);

        // Load test data
        List<Observation> testObservations = DataLoader.loadLanguageData(testDirectory);

        // Classify test data and print results
        System.out.println(classMap);
        for (Observation obs : testObservations) {
            String classification = network.classify(obs);
            System.out.println(obs.getClassification() + " classified as: " + classification);
        }

        // Classify input from user input
        classifyFromSystemInLoop(network);
    }

    // Method to continuously classify user input
    private static void classifyFromSystemInLoop(Network network) {
        Scanner scanner = new Scanner(System.in);
        String text;
        System.out.println("-------------------------------------------------");
        while (true) {

            System.out.println("Enter text:");
            text = scanner.nextLine();
            Observation obs = new Observation(DataLoader.getStatisticsVector(text), "input");
            String classification = network.classify(obs);
            System.out.println(obs.getClassification() + " classified as: " + classification);
        }
    }

    // Method to map observation classifications to unique IDs
    private static Map<String, Integer> mapObservationsToIds(List<Observation> observations) {
        Map<String, Integer> classMap = new HashMap<>();
        observations.stream()
                .map(Observation::getClassification)
                .distinct()
                .forEach(cls -> classMap.put(cls, classMap.size()));
        return classMap;
    }
}

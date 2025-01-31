
public class Dependency {
    public static void main(String[] args) {

        Computer newComputer = new Computer(4070);
        newComputer.checkSpecs();
    }

}

class Computer {

    GpuGreen gpu;

    public Computer(int series) {
        this.gpu = new GpuGreen(series);

    }

    void checkSpecs() {
        System.out.println("This device has " + this.gpu);
    }

}

class GpuGreen {
    int series;

    public GpuGreen(int series) {
        this.series = series;
    }

    @Override
    public String toString() {
        return "GPU Green Series " + this.series;
    }

}
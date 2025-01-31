
public class Injection {
    public static void main(String[] args) {

        GpuGreen greenGpu = new GpuGreen(4070);
        GpuRed redGpu = new GpuRed(7900);
        Computer oldComputer = new Computer(greenGpu);
        oldComputer.checkSpecs();

        Computer newComputer = new Computer(redGpu);
        newComputer.checkSpecs();

    }
}

class Computer {

    Gpu gpu;

    public Computer(Gpu gpu) {
        this.gpu = gpu;

    }

    void checkSpecs() {
        System.out.println("This device has " + this.gpu);
    }

}

class Gpu {

}

class GpuGreen extends Gpu {
    int series;

    public GpuGreen(int series) {
        this.series = series;
    }

    @Override
    public String toString() {
        return "GPU Green Series " + this.series;
    }

}

class GpuRed extends Gpu {
    int series;

    public GpuRed(int series) {
        this.series = series;
    }

    @Override
    public String toString() {
        return "GPU Red Series " + this.series;
    }

}

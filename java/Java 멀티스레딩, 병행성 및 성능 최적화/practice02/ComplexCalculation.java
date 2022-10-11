import java.util.*;
import java.math.BigInteger;

public class ComplexCalculation {
    public BigInteger calculateResult(BigInteger base1, BigInteger power1, BigInteger base2, BigInteger power2) {
        /**
         * Calculate result = ( base1 ^ power1 ) + (base2 ^ power2).
         * where each calculation in (..) is calculated on a different thread
         */
        PowerCalculatingThread thread1 = new PowerCalculatingThread(base1, power1);
        PowerCalculatingThread thread2 = new PowerCalculatingThread(base2, power2);

        thread1.start();
        thread2.start();

        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        return thread1.getResult().add(thread2.getResult());
    }

    private static class PowerCalculatingThread extends Thread {
        private BigInteger result = BigInteger.ONE;
        private BigInteger base;
        private BigInteger power;

        public PowerCalculatingThread(BigInteger base, BigInteger power) {
            this.base = base;
            this.power = power;
        }

        @Override
        public void run() {
            this.result = this.base.pow(this.power.intValue());
        }

        public BigInteger getResult() {
            return result;
        }
    }
}

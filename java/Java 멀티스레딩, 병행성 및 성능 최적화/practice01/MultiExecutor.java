import java.util.*;

public class MultiExecutor {

    private final List<Runnable> tasks;

    /**
     * @param tasks to executed concurrently
     */
    public MultiExecutor(List<Runnable> tasks) {
        this.tasks = tasks;
    }

    /**
     * Starts and executes all the tasks concurrently
     */
    public void executeAll() {
        for (Runnable task : tasks) {
            Thread thread = new Thread(task);
            thread.start();
        }
    }
}
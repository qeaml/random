import java.net.Socket;
import java.net.UnknownHostException;
import java.net.InetSocketAddress;
import java.io.OutputStream;
import java.io.IOException;
import java.util.Scanner;
import java.lang.Thread;
import java.lang.InterruptedException;

public class FileDumperClient {
    /**
    * A method for combining two byte arrays together.
    */
    private static byte[] combine(byte[] one, byte[] two) {
        byte[] combined = new byte[one.length + two.length];

        for (int i = 0; i < combined.length; ++i)
        {
            combined[i] = i < one.length ? one[i] : two[i - one.length];
        }
        
        return combined;
    }
    
    public static void main(String[] argv) {
        Socket sock = new Socket();
        Scanner scan = new Scanner(System.in);
        
        System.out.println("Connecting...");
        
        InetSocketAddress addr = new InetSocketAddress("localhost", 33787);
        try{
            sock.connect(addr);
        } catch(IOException e) {
            System.out.println("An I/O error has occured.");
            System.exit(1);
        }
        
        System.out.println("Connected!");
        
        System.out.println("Enter a filename:");
        String filename = scan.nextLine();
        
        System.out.println("Enter contents:");
        String contents =  scan.nextLine();
        
        System.out.println("Sending...");
        
        byte[] filenamePacket = combine(new byte[]{0x00}, filename.getBytes());
        byte[] contentsPacket = combine(new byte[]{0x0F}, contents.getBytes());
        // javac complains about lossy conversion below but not above. weird.
        byte[] endStreamPacket = new byte[]{(byte)0xFF};
        
        try{
            OutputStream sockStream = sock.getOutputStream();
            sockStream.write(filenamePacket);
            sockStream.write(contentsPacket);
            // we need to wait for a bit because the OutputStream seems to mash
            // the packets together, which isn't what we want.
            Thread.currentThread().sleep(1);
            sockStream.write(endStreamPacket);
            sock.close();
        } catch(IOException e) {
            System.out.println("An I/O error has occured.");
            System.exit(1);
        } catch(InterruptedException e) {
            // this exception will theoretically never occur.
            System.out.println("A thread has interrupted the main thread.");
            System.exit(1);
        }
        
        System.out.println("Done!");
        System.exit(0);
    }
}
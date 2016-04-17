import java.io.*;
import java.util.*;

public class documentchange {
	static String	ERROR_ARGS = "1 The number of arguments is not correct!",
					ERROR_FILE_OPEN = "1 Some wrongs with files' name!",
					ERROR_FILE_READ = "1 Some wrongs with file's content!",
					ERROR_FILE_FORMAT = "1 Some wrongs with the file's format!",
					SUCCEEDED = "0 Successfully change input file into text format!";
//	The first integer indicates the status for this program.
//	With 0 means it succefully finish its task, 1 means some wrongs happend.

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Now starting...");
		if(args.length != 2) {
			System.out.println(ERROR_ARGS);
			return;
		}
		String inputFile = args[0], outputFile = args[1];
		System.out.println(inputFile + " " + outputFile);
		/*try {
			File finput = new File(inputFile);
			File foutput = new File(outputFile);
		}
		catch(Exception e) {
			
		}*/
	}

}

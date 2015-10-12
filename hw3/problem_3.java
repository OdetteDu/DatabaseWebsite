import java.util.*;
import java.io.*;

public class DataGenerator {

	public static void main(String[] args) throws IOException
	{
		Random r = new Random();
		String s = "";
		s = s + "drop table if exists R;\n"+
				"create table R (a int, b int);\n"+
				"drop table if exists S;\n"+
				"create table S (a int, c int);\n\n";

		for(int i=0; i<10000; i++)
		{
			int a = r.nextInt(2);
			int b = r.nextInt(10000);
			s = s + "insert into R values ("+a+","+b+");\n";
		}

		for(int i=0; i<10000; i++)
		{
			int a = 0;
			int b = r.nextInt(10000);
			s = s + "insert into S values ("+a+","+b+");\n";
		}
		
		s += "analyze;\n";

		s = s + "\nexplain select *\n"+
				"from R, S\n"+
				"where R.a = S.a;\n";

		File file =new File("test.sql");

		if(file.exists()){
			
			file.delete();
		}
		file.createNewFile();

		FileWriter fileWritter = new FileWriter(file.getName(),true);
		BufferedWriter bufferWritter = new BufferedWriter(fileWritter);
		bufferWritter.write(s);
		bufferWritter.close();

		String t = "delete from R where a = 0;\n";
		for(int i=0; i<10000; i++)
		{
			int a = 1;
			int b = r.nextInt(1000);
			t += "insert into R values ("+a+","+b+");\n";
		}
		t += "analyze;\n";
		t += "\nexplain select *\n"+
				"from R, S\n"+
				"where R.a = S.a;";
		
		File file2 =new File("test2.sql");

		if(file2.exists()){
			
			file2.delete();
		}
		file2.createNewFile();

		FileWriter fileWritter2 = new FileWriter(file2.getName(),true);
		BufferedWriter bufferWritter2 = new BufferedWriter(fileWritter2);
		bufferWritter2.write(t);
		bufferWritter2.close();
	}
}

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MaxTemp {
	
	public static void main(String[] args) throws Exception{
		if (args.length != 2){
			System.err.println("Usage: MaxTemp <input> <output>");
			System.exit(-1);
		}
		
		Job job = new Job();
		job.setJarByClass(MaxTemp.class);
		job.setJobName("Max Temp HDG");
		
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		
		job.setMapperClass(Chapter2MaxTempMapper.class);
		//If Combiner is wanted
		//job.setCombinerClass(Chapter2MaxTempReducer.class);
		job.setReducerClass(Chapter2MaxTempReducer.class);
		
		System.exit(job.waitForCompletion(true) ? 0 :1);
	}

}

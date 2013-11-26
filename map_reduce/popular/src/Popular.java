package dk.itu.sad2;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.jobcontrol.JobControl;
import org.apache.hadoop.mapreduce.Job;
//import org.apache.hadoop.mapred.jobcontrol.*;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.IOException;
import java.util.StringTokenizer;

/**
 */
public class Popular {

    public static class RoundOneMap extends Mapper<LongWritable, Text, Text, Text> {
        private Text actor = new Text();
        private Text movie = new Text();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            StringTokenizer tokenizer = new StringTokenizer(line);
            actor.set(tokenizer.nextToken());
            while (tokenizer.hasMoreTokens()) {
                movie.set(tokenizer.nextToken());
                context.write(movie, actor);
            }
        }
    }

    public static class RoundOneReduce extends Reducer<Text, Text, Text, Text> {

        public void reduce(Text movie, Iterable<Text> actors, Context context)
                throws IOException, InterruptedException {
            StringBuilder result = new StringBuilder();
            for(Text actor : actors) {
                result.append(actor.toString() + " ");
            }
            context.write(movie, new Text(result.toString()));
        }
    }

    public static class RoundTwoMap extends Mapper<LongWritable, Text, Text, Text> {
        // Input <Movie, Actor>
        // Returns emits <Actor,Actor>

        private Text actor = new Text();
        private Text movie = new Text();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            StringTokenizer tokenizer = new StringTokenizer(line);
            actor.set(tokenizer.nextToken());
            while (tokenizer.hasMoreTokens()) {
                movie.set(tokenizer.nextToken());
                context.write(movie, actor);
            }
        }
    }

    public static class RoundTwoReduce extends Reducer<Text, Text, Text, Text> {

        public void reduce(Text movie, Iterable<Text> actors, Context context)
                throws IOException, InterruptedException {
            StringBuilder result = new StringBuilder();
            for(Text actor : actors) {
                result.append(actor.toString() + " ");
            }
            context.write(movie, new Text(result.toString()));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();

        Job roundOneJob = new Job(conf, "Round01");
        roundOneJob.setJarByClass(dk.itu.sad2.Popular.class);

        roundOneJob.setOutputKeyClass(Text.class);
        roundOneJob.setOutputValueClass(Text.class);

        roundOneJob.setMapperClass(RoundOneMap.class);
        roundOneJob.setReducerClass(RoundOneReduce.class);

        roundOneJob.setInputFormatClass(TextInputFormat.class);
        roundOneJob.setOutputFormatClass(TextOutputFormat.class);

        FileInputFormat.addInputPath(roundOneJob, new Path(args[0]));
        FileOutputFormat.setOutputPath(roundOneJob, new Path(args[1]));


        roundOneJob.waitForCompletion(true);

        if (roundOneJob.isSuccessful()) {
            Job roundTwoJob = new Job(conf, "Round02");
            roundTwoJob.setJarByClass(dk.itu.sad2.Popular.class);

            roundTwoJob.setOutputKeyClass(Text.class);
            roundTwoJob.setOutputValueClass(Text.class);

            roundTwoJob.setMapperClass(RoundTwoMap.class);
            roundTwoJob.setReducerClass(RoundTwoReduce.class);

            roundTwoJob.setInputFormatClass(TextInputFormat.class);
            roundTwoJob.setOutputFormatClass(TextOutputFormat.class);

            FileInputFormat.addInputPath(roundTwoJob, new Path(args[2]));
            FileOutputFormat.setOutputPath(roundTwoJob, new Path(args[3]));
        }
    }

}
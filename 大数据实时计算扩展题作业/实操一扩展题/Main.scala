import org.apache.flink.streaming.api.scala.{StreamExecutionEnvironment, _}
import org.apache.flink.streaming.api.windowing.time.Time

object Main {
  val target = 'b'

  def main(args: Array[String]) {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    //Linux or Mac:nc -l 9999
    //Windows:nc -l -p 9999
    val text = env.socketTextStream("localhost", 9999)
    val stream = text.flatMap {
      _.toLowerCase.split("\\b+") filter {
        _.contains(target)
      }
    }.map(_.count(c => (c == target)))
      .timeWindowAll(Time.minutes(1), Time.seconds(5))
      .sum(0)
      .map("过去一分钟出现了" + _ + "次")

    stream.print()
    env.execute("Window Stream WordCount")
  }
}
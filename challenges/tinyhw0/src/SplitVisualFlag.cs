using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SplitVisualFlag
{
    class Program_old
    {
        public static int splits = 3;
        public static int scale = 2;

        public static int targetWidth = 84;
        //public static int targetHeight = 84;

        static void Main(string[] args)
        {

            for(int i = 1; i< 5;i++)
            {
                worker(i, false);
            }

        }

        static void worker(int fileNumber, bool byColumns = false)
        {
            Bitmap original = new Bitmap($"TestFlag{fileNumber}.bmp");

            Random r = new Random(3);

            Bitmap[] child = new Bitmap[splits];
            for (int i = 0; i < splits; i++)
            {
                //child[i] = new Bitmap(targetWidth, original.Height*scale);
                //69 chosen empiricaly
                child[i] = new Bitmap(targetWidth, 69);
            }


            int startX = targetWidth / 2 - (original.Width * scale) / 2;

            for (int x = 0; x < original.Width; x++)
            {
                int outputLayer = -1;
                if (byColumns)
                    outputLayer = r.Next(splits);
                for (int y = 0; y < original.Height; y++)
                {
                    Color px = original.GetPixel(x, y);
                    //Console.WriteLine($"{px.A:X},{px.R:X},{px.G:X},{px.B:X}");
                    if (px.A == 0xFF)
                    {
                        if (!byColumns)
                            outputLayer = r.Next(splits);
                        floodFill(startX + (x * scale), y * scale, child[outputLayer], px, scale);
                    }
                }
            }

            Bitmap crosscheck = new Bitmap(child[0].Width, child[0].Height);
            for (int x = 0; x < child[0].Width; x++)
            {
                for (int y = 0; y < child[0].Height; y++)
                {
                    Color px2 = new Color();
                    for(int i = 0; i < splits;i++)
                    {
                        px2 = child[i].GetPixel(x, y);
                        if (px2.A == 0xFF)
                        {
                            break;
                        }
                    }

                    crosscheck.SetPixel(x, y, px2);
                }
            }
            crosscheck.Save($"output{fileNumber}-Crosscheck.bmp");

            for (int i = 0; i < splits; i++)
            {
                child[i].Save($"output{fileNumber}-{i}.bmp");
            }
        }

        public static void floodFill(int startX, int startY, Bitmap target, Color c, int size)
        {
            for (int x = startX; x < startX + size; x++)
            {
                for (int y = startY; y < startY + size; y++)
                {
                    target.SetPixel(x, y, c);
                }
            }
        }
    }
}

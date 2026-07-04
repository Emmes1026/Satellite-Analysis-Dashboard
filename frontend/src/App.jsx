import "./App.css"
import { 
  useEffect,
  useState } from "react";
import { 
  Tabs, 
  TabsContent, 
  TabsList, 
  TabsTrigger 
} from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import {
  Field,
  FieldDescription,
  FieldLabel,
} from "@/components/ui/field"
import { Button } from "@/components/ui/button"
import { Spinner } from "@/components/ui/spinner"
import { 
  useQuery, 
  useMutation 
} from "@tanstack/react-query"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"



function App() {

  const [result, setResult] = useState(null);
  const [imageSize, setImageSize] = useState({ width: 1, height: 1 });

  const resultId = result?.id;

  const { data: detections, isFetching, isLoading: isRadarLoading  } = useQuery({
    queryKey: ["detections", resultId],
    queryFn: async () => {
      const response = await fetch(
        "http://localhost:8000/api/detections/" + resultId + "/"
      );

      if (response.status === 404) {
        return null;
      }

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      }

      return await response.json();
    },
    enabled: !!resultId,
    refetchInterval: (query) => {
      const actualData = query.state.data;

      if (actualData && actualData.raw_detections) {
        return false;
      }

      return 2000;
    }
  })

  const isAnalyzing = resultId && !detections?.raw_detections;

  const { mutate: uploadImage } = useMutation({
    mutationFn: async (newImage) => {
      
      const response = await fetch("http://localhost:8000/api/images/", {
        method: "POST",
        body: newImage,
      });
      if (!response.ok) throw new Error("fetch error");
      return response.json();
    },
    onSuccess: (newPhoto) => {
      setResult(newPhoto);
    }
  });

  async function handleSubmit(e) {
    e.preventDefault()
    
    const form = e.target;
    const formData = new FormData(form)

    uploadImage(formData)

  };

  return (
    <div className="min-h-screen flex flex-col">
      <Tabs defaultValue="main" className="flex flex-col grow">

        <div className=" mx-auto border-2 rounded-lg flex place-content-center mt-6 p-2">
            <TabsList>
              <TabsTrigger value="main">Main Page</TabsTrigger>
              <TabsTrigger value="gallery">Gallery</TabsTrigger>
            </TabsList>
        </div>
        
        <TabsContent value="main" className="flex flex-col grow">

          <form className="w-3/4 mx-auto border-2 rounded-lg flex flex-row flex-wrap items-end place-content-center mt-4 p-4 gap-4" onSubmit={handleSubmit}>

            <Field className="max-w-50">
              <FieldLabel htmlFor="input-field-image-name">
                Image name <span className="text-destructive">*</span>
              </FieldLabel>
              <Input name="name" id="input-field-image-name" type="text" placeholder="Enter image name" required/>
            </Field>

            <Field className="max-w-70">
              <FieldLabel htmlFor="input-field-image">
                Image <span className="text-destructive">*</span>
              </FieldLabel>
              <Input name="image" id="input-field-image" type="file" accept="image/*" required/>
            </Field>

            <Field className="max-w-20">
              <FieldLabel htmlFor="input-field-latitude">Latitude (optional)</FieldLabel>
              <Input name="latitude" id="input-field-latitude" type="number" min="-90" max="90" step="any"/>
            </Field>

            <Field className="max-w-20">
              <FieldLabel htmlFor="input-field-longitude">Longitude (optional)</FieldLabel>
              <Input name="longitude" id="input-field-longitude" type="number" min="-180" max="180" step="any"/>
            </Field>

            <Button type="submit" disabled={isAnalyzing} >Submit</Button>

          </form>

          {result && (
            <div className="w-3/4 mx-auto border-2 rounded-lg flex flex-col grow p-4 mt-6 items-center truncate">
              <h1 className="text-xl md:text-3xl font-bold tracking-tight">IMAGE OVERVIEW</h1>
              <p className="text-lg md:text-xl"> {result.name} </p>

              <div className="relative w-fit mx-auto">
                <img src={result.image} onLoad={(e) => setImageSize({ width: e.target.naturalWidth, height: e.target.naturalHeight })} alt="Photo" className="max-w-full max-h-125 rounded-md"/>
                
                {detections?.raw_detections && detections.raw_detections.map((box, index) => {

                  const topPercent = (box.miny / imageSize.height) * 100;
                  const leftPercent = (box.minx / imageSize.width) * 100;
                  const widthPercent = (box.maxx - box.minx) / imageSize.width * 100;
                  const heightPercent = (box.maxy - box.miny) / imageSize.height * 100;


                  return (
                    <div 
                      key={index}
                      className="absolute border-2 border-red-500 bg-red-500/20" 
                      style={{
                        top: `${topPercent}%`,
                        left: `${leftPercent}%`,
                        width: `${widthPercent}%`,
                        height: `${heightPercent}%`
                      }}
                    >
                      <span className="absolute -top-5 left-0 bg-red-500 text-white text-xs px-1 rounded whitespace-nowrap">
                        {box.name} {(box.score_value * 100).toFixed(0)}%
                      </span>
                    </div>
                  );
                })}

                {isAnalyzing && (
                  <div className="absolute inset-0 flex items-center justify-center bg-background/50 rounded-md z-10">
                    <Spinner/>
                  </div>
                )}
              </div>
            </div>
          )}


          <div className="flex">
          </div>          
        </TabsContent>

        <TabsContent value="gallery">

        </TabsContent>

      </Tabs>
    </div>

  )
}
export default App



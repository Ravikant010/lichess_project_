import instance from "@/api/API";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [TopPlayers, setTopPlayers] = useState([]);
  const [RatingHistoryUser, setRatingUser] = useState("");
  const [RatingHistory, setRatingHistory] = useState([]);
  const [Columns, setColumns] = useState([]);
  async function handleTopPlayetData() {
    const { data } = await instance.get("/top-players", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    console.log(data);
    if (data) {
      setTopPlayers(data?.users);
    }
  }

  async function userRatingHistory() {
    const { data } = await instance.get(
      `/player/${RatingHistoryUser}/rating-history`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    setRatingHistory(data[0].rating[0].points?.slice(0, 50));
    const ColumnsHeadings = data[0].rating.map((item) => item.name);
    setColumns(ColumnsHeadings);

    console.log(RatingHistory);
  }

  useEffect(() => {
    handleTopPlayetData();
  }, []);
  useEffect(() => {
    console.log(TopPlayers);
  }, [TopPlayers]);

  useEffect(() => {
    if (RatingHistory) {
      userRatingHistory();
    }
  }, [RatingHistoryUser]);
const navigate = useNavigate()
  if (RatingHistoryUser) {
    return (
      <>
        <div className="flex items-center justify-center py-6 font-sans text-xl font-medium text-center capitalize">
          <div className="relative w-full py-5 bg-zinc-300 bg-opacity-30">{RatingHistoryUser} rating history{" "}</div>
          <Button className="absolute right-0 mr-6 px-7" onClick={()=>{
            setRatingUser('')
          }}>Exit</Button>
        </div>
        <Table className="capitalize ">
          <TableHeader>
            <TableRow>
              {/* <TableHead className="w-[100px]">id</TableHead> */}
              {/* <TableHead>Date</TableHead>
               */}
              <TableHead>id</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>{Columns[0]}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody className="">
            {RatingHistory &&
              RatingHistory.map((e, index) => {
                return (
                  <TableRow>
                    <TableCell>{index+1}</TableCell>
                    <TableCell>
                   {e[2]}/{e[1]}/{e[2]} 
                    </TableCell>
                    <TableCell>{e[3]}</TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </>
    );
  }
  return (
    <>
      <div className="flex items-center py-6 font-sans text-xl font-medium text-center">
       <div className="w-full text-center"> Chess Players Data{" "}</div>
      <Button className="absolute right-0 mr-6 px-7" onClick={()=>{
        localStorage.removeItem("token")
        navigate("/login")
      }}>Logout</Button>
      </div>
      <Table className="capitalize ">
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">id</TableHead>
            <TableHead>username</TableHead>
            <TableHead>rating</TableHead>
            <TableHead className="">progress</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody className="">
          {TopPlayers &&
            TopPlayers.map((el, index) => {
              return (
                <TableRow
                  onClick={() => {
                    setRatingUser(el?.username as string);
                  }}
                >
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{el?.username as string}</TableCell>
                  <TableCell>{el?.perfs?.bullet?.rating}</TableCell>
                  <TableCell>{el?.perfs?.bullet?.progress + "%"}</TableCell>
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </>
  );
};

export default Dashboard;
